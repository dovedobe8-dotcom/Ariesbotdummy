# Facebook Realtime WebSocket connection for notifications, friend requests, and presence updates

from __future__ import annotations

import asyncio
import struct
import aiohttp
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Callable
from urllib.parse import urlencode
from yarl import URL

from .state import State
from .logging.logger import get_logger
from .exception.errors import FBChatError
@dataclass 
class NotificationEvent:
    type: str 
    notif_id: str
    body: str | None 
    sender_id: str
    url: str | None
    timestamp: int
    seen_state: Any 
    raw_data: Any


logger = get_logger()


class RealtimeEventEmitter:
    """Event emitter for realtime WebSocket events"""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._running = True
    
    def on(self, event: str, callback: Callable):
        """Register an event listener"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
        logger.debug(f"Registered listener for event: {event}")
    
    def off(self, event: str, callback: Callable):
        """Remove an event listener"""
        if event in self._listeners:
            try:
                self._listeners[event].remove(callback)
                if not self._listeners[event]:
                    del self._listeners[event]
            except ValueError:
                pass
    
    async def emit(self, event: str, *args, **kwargs):
        """Emit an event to all listeners"""
        if not self._running or event not in self._listeners:
            return
            
        for callback in self._listeners[event][:]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(*args, **kwargs)
                else:
                    callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in event listener for {event}: {e}")
                if event != 'error':
                    await self.emit('error', e)
    
    def stop(self):
        """Stop the event emitter"""
        self._running = False
        self._listeners.clear()

def format_notification(data: Dict[str, Any]) -> Optional[NotificationEvent]:
    """Format notification data from WebSocket response"""
    try:
        if not data.get('data') or not data['data'].get('viewer'):
            return None
        
        notif_edge = (data['data']['viewer']
                     .get('notifications_page', {})
                     .get('edges', [{}])[1:2])
        
        if not notif_edge:
            return None
            
        notif = notif_edge[0].get('node', {}).get('notif')
        if not notif:
            return None
        
        # Extract sender ID from tracking
        tracking = notif.get('tracking', {})
        from_uids = tracking.get('from_uids', {})
        sender_id = next(iter(from_uids.keys())) if from_uids else None
        
        return NotificationEvent(
            type="notification",
            notif_id=notif.get('notif_id'),
            body=notif.get('body', {}).get('text') if notif.get('body') else None,
            sender_id=sender_id or "",
            url=notif.get('url'),
            timestamp=notif.get('creation_time', {}).get('timestamp'),
            seen_state=notif.get('seen_state'),
            raw_data=data
        )
        
    except Exception as e:
        logger.error(f"Error formatting notification: {e}")
        return None

def get_cookie_header(session: aiohttp.ClientSession, url: str) -> str:
    """Extract cookies for the given URL"""
    return session.cookie_jar.filter_cookies(URL(url)).output(header="", sep=";").lstrip()

@dataclass
class FacebookRealtime:
    """Facebook WebSocket realtime connection handler"""
    
    _state: State = field()
    _ws: Optional[aiohttp.ClientWebSocketResponse] = field(default=None)
    _session: Optional[aiohttp.ClientSession] = field(default=None)
    _emitter: RealtimeEventEmitter = field(default_factory=RealtimeEventEmitter)
    _listen_task: Optional[asyncio.Task] = field(default=None)
    _running: bool = field(default=False)
    _message_handler: Optional[Callable] = field(default=None)
    
    # WebSocket connection parameters
    _WS_HOST = "wss://gateway.facebook.com/ws/realtime"
    _APP_ID = "2220391788200892"
    
    @classmethod
    async def connect(cls, state: State, message_handler: Callable) -> FacebookRealtime:
        """Create and connect to Facebook realtime WebSocket"""
        instance = cls(_state=state, _message_handler=message_handler)
        await instance._connect()
        return instance
    
    def _get_subscriptions(self) -> List[str]:
        """Get list of subscription payloads for different Facebook services"""
        user_id = self._state.user_id
        
        return [
            '{"x-dgw-app-XRSS-method":"Falco","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com"}',
            '{"x-dgw-app-XRSS-method":"FBGQLS:USER_ACTIVITY_UPDATE_SUBSCRIBE","x-dgw-app-XRSS-doc_id":"9525970914181809","x-dgw-app-XRSS-routing_hint":"UserActivitySubscription","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com"}',
            '{"x-dgw-app-XRSS-method":"FBGQLS:ACTOR_GATEWAY_EXPERIENCE_SUBSCRIBE","x-dgw-app-XRSS-doc_id":"24191710730466150","x-dgw-app-XRSS-routing_hint":"CometActorGatewayExperienceSubscription","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com"}',
            f'{{"x-dgw-app-XRSS-method":"FBLQ:comet_notifications_live_query_experimental","x-dgw-app-XRSS-doc_id":"9784489068321501","x-dgw-app-XRSS-actor_id":"{user_id}","x-dgw-app-XRSS-page_id":"{user_id}","x-dgw-app-XRSS-request_stream_retry":"false","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com"}}',
            '{"x-dgw-app-XRSS-method":"FBGQLS:FRIEND_REQUEST_CONFIRM_SUBSCRIBE","x-dgw-app-XRSS-doc_id":"9687616244672204","x-dgw-app-XRSS-routing_hint":"FriendingCometFriendRequestConfirmSubscription","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com"}',
            '{"x-dgw-app-XRSS-method":"FBGQLS:FRIEND_REQUEST_RECEIVE_SUBSCRIBE","x-dgw-app-XRSS-doc_id":"24047008371656912","x-dgw-app-XRSS-routing_hint":"FriendingCometFriendRequestReceiveSubscription","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com"}',
            '{"x-dgw-app-XRSS-method":"FBGQLS:RTWEB_CALL_BLOCKED_SETTING_SUBSCRIBE","x-dgw-app-XRSS-doc_id":"24429620016626810","x-dgw-app-XRSS-routing_hint":"RTWebCallBlockedSettingSubscription_CallBlockSettingSubscription","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com"}',
            '{"x-dgw-app-XRSS-method":"PresenceUnifiedJSON","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com/friends"}',
            '{"x-dgw-app-XRSS-method":"FBGQLS:MESSENGER_CHAT_TABS_NOTIFICATION_SUBSCRIBE","x-dgw-app-XRSS-doc_id":"23885219097739619","x-dgw-app-XRSS-routing_hint":"MWChatTabsNotificationSubscription_MessengerChatTabsNotificationSubscription","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com/friends"}',
            '{"x-dgw-app-XRSS-method":"FBGQLS:BATCH_NOTIFICATION_STATE_CHANGE_SUBSCRIBE","x-dgw-app-XRSS-doc_id":"30300156509571373","x-dgw-app-XRSS-routing_hint":"CometBatchNotificationsStateChangeSubscription","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com/friends"}',
            '{"x-dgw-app-XRSS-method":"FBGQLS:NOTIFICATION_STATE_CHANGE_SUBSCRIBE","x-dgw-app-XRSS-doc_id":"23864641996495578","x-dgw-app-XRSS-routing_hint":"CometNotificationsStateChangeSubscription","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com"}',
            '{"x-dgw-app-XRSS-method":"FBGQLS:NOTIFICATION_STATE_CHANGE_SUBSCRIBE","x-dgw-app-XRSS-doc_id":"9754477301332178","x-dgw-app-XRSS-routing_hint":"CometFriendNotificationsStateChangeSubscription","x-dgw-app-xrs-body":"true","x-dgw-app-XRS-Accept-Ack":"RSAck","x-dgw-app-XRSS-http_referer":"https://www.facebook.com"}'
        ]
    
    async def _connect(self):
        """Establish WebSocket connection to Facebook realtime gateway"""
        try:
            # Build query parameters
            query_params = {
                "x-dgw-appid": self._APP_ID,
                "x-dgw-appversion": "0",
                "x-dgw-authtype": "1:0",
                "x-dgw-version": "5",
                "x-dgw-uuid": str(self._state.user_id),
                "x-dgw-tier": "prod",
                "x-dgw-deviceid": self._state._mqttClientID,
                "x-dgw-app-stream-group": "group1"
            }
            
            url = f"{self._WS_HOST}?{urlencode(query_params)}"
            
            # Get cookies
            cookies = get_cookie_header(self._state._session, "https://www.facebook.com")
            
            # Build headers
            headers = {
                "Cookie": cookies,
                "Origin": "https://www.facebook.com",
                "User-Agent": self._state._userAgent,
                "Referer": "https://www.facebook.com",
                "Host": URL(url).host,
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9"
            }
            
            logger.debug(f"📤 Connecting to Facebook realtime WebSocket: {url}")
            # logger.debug(f"Headers: {headers}")
            
            # Create WebSocket session
            self._session = self._state._session
            self._ws = await self._session.ws_connect(url, headers=headers, heartbeat=20, autoping=True)
            
            logger.info("Connected to Facebook realtime WebSocket")
            
            # Send subscriptions
            await self._send_subscriptions()
            
            # Start background tasks
            self._running = True
            self._listen_task = asyncio.create_task(self._listen_loop())
            
            await self._emitter.emit('connected')
            
        except Exception as e:
            logger.error(f"💥 Connection error: {e}")
            await self._emitter.emit('error', e)
            # Schedule reconnection
            asyncio.create_task(self._schedule_reconnect())
    
    async def _send_subscriptions(self):
        """Send subscription messages to Facebook gateway"""
        subscriptions = self._get_subscriptions()
        
        logger.debug(f"📤 Sending subscription...")
        for index, payload in enumerate(subscriptions):
            try:
                # Format: [14, index, 0, payload_length] + payload + [0, 0]
                prefix = struct.pack('BBBi', 14, index, 0, len(payload))
                suffix = struct.pack('BB', 0, 0)
                full_message = prefix + payload.encode('utf-8') + suffix
                if self._ws: 
                    await self._ws.send_bytes(full_message)
                
            except Exception as e:
                logger.error(f"Error sending subscription {index}: {e}")
                if self._running:
                    logger.debug("Attempting to reconnect realtime..")
                    await self.reconnect()
        logger.debug(f"Successfully sent subscriptions!")
    
    async def _listen_loop(self):
        """Main message listening loop"""
        if not self._ws:
            raise FBChatError("Websocket not initilised for listening to realtime events")
        try:
            async for msg in self._ws:
                if self._message_handler:
                    await self._message_handler(msg.type, msg.data)
        except asyncio.CancelledError:
            logger.debug("🛑 Realtime loop cancelled")
            return
        except Exception as e:
            logger.error(f"Error in listen loop: {e}")
            await self._emitter.emit('error', e)

    async def listen(self):
        if self._listen_task:
            await self._listen_task

    def set_message_handler(self, handler: Callable):
        """Set the message handler function"""
        self._message_handler = handler


    async def _schedule_reconnect(self):
        """Schedule reconnection after a delay"""
        if not self._running:
            return
            
        logger.warning("🔌 Scheduling reconnection in 1 second...")
        await asyncio.sleep(1)
        
        if self._running:
            await self.reconnect()


    async def reconnect(self):
        await self._cleanup()
        await self._connect()

    
    async def _cleanup(self):
        """Clean up resources"""
        # Close WebSocket
        if self._ws and not self._ws.closed:
            await self._ws.close()
        
        # Close _session
        self._session = None


    def on(self, event: str, callback: Callable):
        """Register event listener"""
        self._emitter.on(event, callback)
    
    def off(self, event: str, callback: Callable):
        """Remove event listener"""
        self._emitter.off(event, callback)
    
    async def stop(self):
        """Stop the realtime connection"""
        logger.debug("Stopping Facebook realtime connection...")
        self._running = False
        self._emitter.stop()
        
        # Cancel reconnect task
        if self._listen_task and not self._listen_task.done():
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
        
        await self._cleanup()
        logger.info("Facebook realtime connection stopped")

