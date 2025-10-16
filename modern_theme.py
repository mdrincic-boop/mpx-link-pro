import tkinter as tk
from tkinter import ttk

class ModernTheme:
    """Modern color scheme and styling for MPX over IP Pro"""

    # Modern color palette - Dark theme
    DARK = {
        'bg_primary': '#0f172a',        # Slate 900
        'bg_secondary': '#1e293b',      # Slate 800
        'bg_tertiary': '#334155',       # Slate 700
        'bg_card': '#1e293b',
        'border': '#475569',            # Slate 600
        'text_primary': '#f1f5f9',      # Slate 100
        'text_secondary': '#cbd5e1',    # Slate 300
        'text_muted': '#94a3b8',        # Slate 400
        'accent_blue': '#3b82f6',       # Blue 500
        'accent_cyan': '#06b6d4',       # Cyan 500
        'success': '#10b981',           # Green 500
        'warning': '#f59e0b',           # Amber 500
        'danger': '#ef4444',            # Red 500
        'vu_green': '#22c55e',          # Green 500
        'vu_yellow': '#facc15',         # Yellow 400
        'vu_red': '#ef4444',            # Red 500
        'vu_bg': '#0f172a',
    }

    # Modern color palette - Light theme
    LIGHT = {
        'bg_primary': '#ffffff',
        'bg_secondary': '#f8fafc',      # Slate 50
        'bg_tertiary': '#e2e8f0',       # Slate 200
        'bg_card': '#ffffff',
        'border': '#cbd5e1',            # Slate 300
        'text_primary': '#0f172a',      # Slate 900
        'text_secondary': '#475569',    # Slate 600
        'text_muted': '#64748b',        # Slate 500
        'accent_blue': '#2563eb',       # Blue 600
        'accent_cyan': '#0891b2',       # Cyan 600
        'success': '#059669',           # Green 600
        'warning': '#d97706',           # Amber 600
        'danger': '#dc2626',            # Red 600
        'vu_green': '#16a34a',          # Green 600
        'vu_yellow': '#eab308',         # Yellow 500
        'vu_red': '#dc2626',            # Red 600
        'vu_bg': '#f1f5f9',
    }

    # Modern fonts
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),
        'heading': ('Segoe UI', 16, 'bold'),
        'subheading': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'mono': ('Consolas', 10),
    }

    def __init__(self, theme='dark'):
        self.theme = theme
        self.colors = self.DARK if theme == 'dark' else self.LIGHT

    def apply_to_root(self, root):
        """Apply modern theme to root window"""
        root.configure(bg=self.colors['bg_primary'])

        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')

        # Configure Frame
        style.configure('TFrame', background=self.colors['bg_primary'])
        style.configure('Card.TFrame',
                       background=self.colors['bg_card'],
                       relief='flat',
                       borderwidth=1)

        # Configure Label
        style.configure('TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=self.FONTS['body'])

        style.configure('Title.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=self.FONTS['title'])

        style.configure('Heading.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=self.FONTS['heading'])

        style.configure('Muted.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_muted'],
                       font=self.FONTS['small'])

        # Configure Button
        style.configure('TButton',
                       background=self.colors['accent_blue'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10),
                       font=self.FONTS['body'])

        style.map('TButton',
                 background=[('active', self.colors['accent_cyan']),
                           ('disabled', self.colors['bg_tertiary'])])

        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white')

        style.configure('Danger.TButton',
                       background=self.colors['danger'],
                       foreground='white')

        # Configure Entry
        style.configure('TEntry',
                       fieldbackground=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['border'],
                       darkcolor=self.colors['border'],
                       insertcolor=self.colors['text_primary'],
                       padding=8)

        # Configure Combobox
        style.configure('TCombobox',
                       fieldbackground=self.colors['bg_secondary'],
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       bordercolor=self.colors['border'],
                       arrowcolor=self.colors['text_primary'],
                       padding=8)

        # Configure Checkbutton
        style.configure('TCheckbutton',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=self.FONTS['body'])

        # Configure Radiobutton
        style.configure('TRadiobutton',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=self.FONTS['body'])

        # Configure LabelFrame
        style.configure('TLabelframe',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       bordercolor=self.colors['border'],
                       relief='flat',
                       borderwidth=2)

        style.configure('TLabelframe.Label',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       font=self.FONTS['subheading'])

        # Configure Notebook
        style.configure('TNotebook',
                       background=self.colors['bg_primary'],
                       borderwidth=0)

        style.configure('TNotebook.Tab',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       padding=(20, 10),
                       borderwidth=0,
                       font=self.FONTS['body'])

        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['bg_primary'])],
                 foreground=[('selected', self.colors['accent_blue'])],
                 expand=[('selected', [1, 1, 1, 0])])

        # Configure Separator
        style.configure('TSeparator',
                       background=self.colors['border'])

    def get_vu_color(self, db_value):
        """Get VU meter color based on dB value"""
        if db_value > -6:
            return self.colors['vu_red']
        elif db_value > -18:
            return self.colors['vu_yellow']
        else:
            return self.colors['vu_green']

    def create_gradient(self, canvas, width, height, color_start, color_end):
        """Create a gradient on canvas"""
        r1, g1, b1 = self.hex_to_rgb(color_start)
        r2, g2, b2 = self.hex_to_rgb(color_end)

        for i in range(width):
            ratio = i / width
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(i, 0, i, height, fill=color)

    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
