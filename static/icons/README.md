# Icon Library

This directory contains all the icons used in the Vacation Club Member Portal application.

## Icon Specifications
- Format: PNG
- Recommended size: 24x24px (for small icons) or 32x32px (for larger icons)
- Background: Transparent
- Color: Can be any color (will be styled via CSS if needed)

## Icon List

### User Interface Icons
- `sign-out.png` - Diagonal arrow (↗️) for sign out button
- `edit.png` - Pencil icon for edit functionality
- `close.png` - X or close icon for modals
- `user.png` - User/person icon for profile
- `email.png` - Email/envelope icon
- `phone.png` - Phone icon
- `membership.png` - Membership card or badge icon
- `calendar.png` - Calendar icon for dates
- `clock.png` - Clock icon for time-related info

### Action Icons
- `save.png` - Save icon for save actions
- `cancel.png` - Cancel icon for cancel actions
- `reset.png` - Reset/refresh icon for password reset

### Feature Icons (for future cards)
- `marketplace.png` - Icon for tokenized points marketplace
- `swap.png` - Icon for token swapping
- `booking.png` - Icon for booking/availability
- `shield.png` - Icon for buy-back program
- `vacation.png` - Icon for vacation booking

## Usage
Icons should be referenced using relative paths from the templates directory:
```html
<img src="../static/icons/icon-name.png" alt="Description" width="16" height="16">
```

## File Naming Convention
- Use lowercase letters
- Use hyphens to separate words
- Include descriptive names
- Example: `sign-out.png`, `edit-profile.png`, `user-avatar.png`
