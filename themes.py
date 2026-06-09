from msgspec import Struct, field
from typing import List, Optional
from .deltas.custom_type import Value


class Asset(Struct, frozen=True):
    """Represents a theme asset (icon or background)"""
    id: str
    """image Id"""
    image: Value
    """Image url"""


class AlternativeTheme(Struct, frozen=True):
    """Alternative theme variant (typically dark mode)"""
    id: str
    accessibility_label: str
    description: Optional[str]
    app_color_mode: str
    composer_background_color: Optional[str]
    background_gradient_colors: List[str]
    is_deprecated: bool
    title_bar_button_tint_color: Optional[str]
    inbound_message_gradient_colors: List[str]
    title_bar_text_color: Optional[str]
    composer_tint_color: Optional[str]
    title_bar_attribution_color: Optional[str]
    composer_input_background_color: Optional[str]
    hot_like_color: Optional[str]
    background_asset: Optional[Asset]
    message_text_color: Optional[str]
    message_border_color: Optional[str]
    message_border_width: Optional[int]
    inbound_message_text_color: Optional[str]
    inbound_message_border_color: Optional[str]
    inbound_message_border_width: Optional[int]
    normal_theme_id: str
    primary_button_background_color: Optional[str]
    title_bar_background_color: Optional[str]
    tertiary_text_color: Optional[str]
    reverse_gradients_for_radial: bool
    reaction_pill_background_color: Optional[str]
    secondary_text_color: Optional[str]
    fallback_color: Optional[str]
    gradient_colors: List[str]
    icon_asset: Optional[Asset]


class Theme(Struct, frozen=True):
    """Main theme information"""
    id: str
    accessibility_label: str
    description: Optional[str]
    app_color_mode: str
    composer_background_color: Optional[str]
    background_gradient_colors: List[str]
    is_deprecated: bool
    title_bar_button_tint_color: Optional[str]
    inbound_message_gradient_colors: List[str]
    title_bar_text_color: Optional[str]
    composer_tint_color: Optional[str]
    title_bar_attribution_color: Optional[str]
    composer_input_background_color: Optional[str]
    hot_like_color: Optional[str]
    background_asset: Optional[Asset]
    message_text_color: Optional[str]
    message_border_color: Optional[str]
    message_border_width: Optional[int]
    inbound_message_text_color: Optional[str]
    inbound_message_border_color: Optional[str]
    inbound_message_border_width: Optional[int]
    primary_button_background_color: Optional[str]
    title_bar_background_color: Optional[str]
    tertiary_text_color: Optional[str]
    reverse_gradients_for_radial: bool
    reaction_pill_background_color: Optional[str]
    secondary_text_color: Optional[str]
    fallback_color: Optional[str]
    gradient_colors: List[str]
    normal_theme_id: str
    icon_asset: Optional[Asset]
    alternative_themes: List[AlternativeTheme]


class ThreadThemes(Struct, frozen=True):
    """Container for messenger thread themes"""
    themes: List[Theme] = field(name="messenger_thread_themes")


class ThemeData(Struct, frozen=True):
    """Root theme data structure"""
    data: ThreadThemes


