# Updated Pinellone Drawing Rules

## New Drawing System

### First Turn Rule
At the start of the game, the discard pile is empty, and the first player must draw two cards from the deck.

### Overview
The game now features an intuitive drawing interface that enforces the Pinellone rule: **players must add two or more cards to their hand on their turn**.

### Drawing Options

#### Option 1: Draw from Deck
- **Action**: Draw 2 cards directly from the deck
- **Requirement**: At least 2 cards must be available in the deck
- **Interface**: Click the deck button or use the drawing modal

#### Option 2: Draw from Discard Pile
- **Action**: Draw 1 card from the deck + any number of cards from the discard pile
- **Process**:
  1. Always draw 1 card from the deck first
  2. Select a card from the discard pile
  3. Take the selected card + all cards above it in the discard pile
- **Example**: If you select the 3rd card from the top of discard, you get cards 3, 4, 5, etc.

### User Interface Features

#### Drawing Selection Modal
- **Visual Preview**: Shows exactly what cards will be drawn
- **Real-time Updates**: Hand count updates immediately after drawing
- **Validation**: Prevents invalid moves with clear error messages
- **Language Support**: Fully translated interface (IT/EN)

#### Language Toggle
- **Location**: Top-right corner of the screen
- **Functionality**: Instant language switching for all UI elements
- **Supported Languages**: Italian (IT) and English (EN)
- **Scope**: All labels, tooltips, rules, and error messages

### API Endpoints

#### Drawing Cards
```
POST /games/{game_id}/draw
{
  "draw_type": "deck" | "discard",
  "card_index": int (optional, for discard draws)
}
```

#### Preview Drawing
```
POST /games/{game_id}/draw-preview
{
  "draw_type": "deck" | "discard",
  "card_index": int (optional)
}
```

### Validation Rules

1. **Phase Check**: Must be in DRAW phase
2. **Deck Check**: Must have sufficient cards (1 for discard, 2 for deck)
3. **Discard Check**: Must have cards in discard pile for discard draws
4. **Index Check**: Discard index must be valid

### Error Handling

- **Insufficient Deck**: "Not enough cards in deck"
- **Invalid Phase**: "Cannot draw cards in current phase"
- **Invalid Index**: "Invalid discard pile selection"
- **Empty Discard**: "Discard pile is empty"

### Frontend Components

#### DrawingSelectionModal
- Modal dialog for selecting drawing source
- Visual representation of discard pile
- Card preview functionality
- Real-time validation feedback

#### LanguageToggle
- Flag-based toggle button
- Persistent language preference
- Smooth transitions between languages

### Testing

Run the new drawing system tests:
```bash
cd pinellone-modern/backend
pytest tests/test_new_drawing_system.py -v

cd pinellone-modern/frontend
npm test DrawingSelectionModal
```

### Integration Notes

The new system maintains backward compatibility while adding:
- Enhanced user experience
- Clear rule enforcement
- Multi-language support
- Real-time feedback
- Comprehensive error handling