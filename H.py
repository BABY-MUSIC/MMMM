from typing import Union
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def help_pannel(_, START: Union[bool, int] = None):
    # Default button configurations
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"], callback_data="settingsback_helper"
        ),
        InlineKeyboardButton(
            text=_["CLOSEMENU_BUTTON"] if "CLOSEMENU_BUTTON" in _ else "Close Menu",
            callback_data="close",
        ),
    ]

    # Choose the appropriate marking based on the START value
    mark = second if START else first

    # Keyboard layout
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴧᴅᴍɪɴ", callback_data="help_callback hb1"),
                InlineKeyboardButton(text="▪️ᴧᴜᴛʜ▪️", callback_data="help_callback hb2"),
            ],
            [
                InlineKeyboardButton(text="ʙʟᴏᴄᴋ", callback_data="help_callback hb3"),
                InlineKeyboardButton(text="ɢ-ᴄᴧsᴛ", callback_data="help_callback hb4"),
            ],
            [
                InlineKeyboardButton(text="ɢ-ʙᴧɴ", callback_data="help_callback hb12"),
                InlineKeyboardButton(text="▪️ʟʏʀɪᴄs▪️", callback_data="help_callback hb5"),
            ],
            [
                InlineKeyboardButton(
                    text="▫️ᴘʟᴀʏʟɪsᴛs▫️", callback_data="help_callback hb6"
                ),
                InlineKeyboardButton(
                    text="ᴠᴏɪᴄᴇ-ᴄʜᴀᴛ", callback_data="help_callback hb10"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔸UNTOLD CODER🔸", url="https://t.me/UNTOLD_CODER4"
                ),
                InlineKeyboardButton(
                    text="▪️ABOUT UNTOLD▪️", url="https://t.me/UNTOLD_CODER"
                ),
            ],
            [
                InlineKeyboardButton(text="▫️ᴘʟᴀʏ▫️", callback_data="help_callback hb8"),
                InlineKeyboardButton(text="sᴜᴅᴏ", callback_data="help_callback hb9"),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_1"], callback_data="help_callback hb1"
                ),
                InlineKeyboardButton(
                    text=_["H_B_2"], callback_data="help_callback hb2"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_3"], callback_data="help_callback hb3"
                ),
                InlineKeyboardButton(
                    text=_["H_B_4"], callback_data="help_callback hb4"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_12"], callback_data="help_callback hb12"
                ),
                InlineKeyboardButton(
                    text=_["H_B_5"], callback_data="help_callback hb5"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_6"], callback_data="help_callback hb6"
                ),
                InlineKeyboardButton(
                    text=_["H_B_10"], callback_data="help_callback hb10"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_8"], callback_data="help_callback hb8"
                ),
                InlineKeyboardButton(
                    text=_["H_B_9"], callback_data="help_callback hb9"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_11"], callback_data="help_callback hb11"
                ),
                InlineKeyboardButton(
                    text="▪️ sᴛᴀʀᴛ ▪️", callback_data="help_callback hb11"
                ),
            ],
            mark,  # Adds the `first` or `second` row based on START
        ]
    )
    return upl







from typing import Union
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def help_pannel(_, START: Union[bool, int] = None):
    # Default button configurations
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"], callback_data="settingsback_helper"
        ),
        InlineKeyboardButton(
            text=_["CLOSEMENU_BUTTON"] if "CLOSEMENU_BUTTON" in _ else "Close Menu",
            callback_data="close",
        ),
    ]

    # Choose the appropriate marking based on the START value
    mark = second if START else first

    # Keyboard layout
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴧᴅᴍɪɴ", callback_data="help_callback hb1"),
                InlineKeyboardButton(text="▪️ᴧᴜᴛʜ▪️", callback_data="help_callback hb2"),
            ],
            [
                InlineKeyboardButton(text="ʙʟᴏᴄᴋ", callback_data="help_callback hb3"),
                InlineKeyboardButton(text="ɢ-ᴄᴧsᴛ", callback_data="help_callback hb4"),
            ],
            [
                InlineKeyboardButton(text="ɢ-ʙᴧɴ", callback_data="help_callback hb12"),
                InlineKeyboardButton(text="▪️ʟʏʀɪᴄs▪️", callback_data="help_callback hb5"),
            ],
            [
                InlineKeyboardButton(
                    text="▫️ᴘʟᴀʏʟɪsᴛs▫️", callback_data="help_callback hb6"
                ),
                InlineKeyboardButton(
                    text="ᴠᴏɪᴄᴇ-ᴄʜᴀᴛ", callback_data="help_callback hb10"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔸UNTOLD CODER🔸", url="https://t.me/UNTOLD_CODER4"
                ),
                InlineKeyboardButton(
                    text="▪️ABOUT UNTOLD▪️", url="https://t.me/UNTOLD_CODER"
                ),
            ],
            [
                InlineKeyboardButton(text="▫️ᴘʟᴀʏ▫️", callback_data="help_callback hb8"),
                InlineKeyboardButton(text="sᴜᴅᴏ", callback_data="help_callback hb9"),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_1"], callback_data="help_callback hb1"
                ),
                InlineKeyboardButton(
                    text=_["H_B_2"], callback_data="help_callback hb2"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_3"], callback_data="help_callback hb3"
                ),
                InlineKeyboardButton(
                    text=_["H_B_4"], callback_data="help_callback hb4"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_12"], callback_data="help_callback hb12"
                ),
                InlineKeyboardButton(
                    text=_["H_B_5"], callback_data="help_callback hb5"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_6"], callback_data="help_callback hb6"
                ),
                InlineKeyboardButton(
                    text=_["H_B_10"], callback_data="help_callback hb10"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_8"], callback_data="help_callback hb8"
                ),
                InlineKeyboardButton(
                    text=_["H_B_9"], callback_data="help_callback hb9"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_7"], callback_data="help_callback hb7"
                ),
                InlineKeyboardButton(
                    text=_["H_B_19"], callback_data="help_callback hb19"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_14"], callback_data="help_callback hb14"
                ),
                InlineKeyboardButton(
                    text=_["H_B_15"], callback_data="help_callback hb15"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_16"], callback_data="help_callback hb16"
                ),
                InlineKeyboardButton(
                    text=_["H_B_17"], callback_data="help_callback hb17"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_18"], callback_data="help_callback hb18"
                ),
                InlineKeyboardButton(
                    text=_["H_B_13"], callback_data="help_callback hb13"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_20"], callback_data="help_callback hb20"
                ),
                InlineKeyboardButton(
                    text=_["H_B_22"], callback_data="help_callback hb22"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_21"], callback_data="help_callback hb21"
                )
            ],
            mark,  # Adds the `first` or `second` row based on START
        ]
    )
    return upl
