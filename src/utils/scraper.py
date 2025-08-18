import random
import time
import logging

logger = logging.getLogger(__name__)


def human_type(element, text: str):
    """Simulate human-like typing with random delays, errors, and variable speed"""
    logger.info(f"Starting human_type for text of length {len(text)}")
    
    try:
        element.click()
        element.fill('')  # Clear field first
        logger.debug("Element clicked and cleared")
        
        i = 0
        while i < len(text):
            char = text[i]
            
            # 3% chance of typing a wrong character first
            if random.random() < 0.03 and i > 0:
                wrong_chars = 'abcdefghijklmnopqrstuvwxyz'
                wrong_char = random.choice(wrong_chars)
                element.type(wrong_char)
                logger.debug(f"Typed wrong character '{wrong_char}' at position {i}")
                
                # Pause as if realizing the mistake
                time.sleep(random.uniform(0.2, 0.5))
                
                # Backspace to correct
                element.press('Backspace')
                time.sleep(random.uniform(0.1, 0.3))
                logger.debug("Corrected typing mistake")
            
            # Type the correct character
            element.type(char)
            
            # Variable typing speed - faster for common sequences, slower for complex parts
            if char.isalpha() and i > 0 and text[i-1].isalpha():
                # Faster for letter sequences (words)
                delay = random.uniform(0.03, 0.08)
            elif char.isdigit():
                # Slower for numbers
                delay = random.uniform(0.08, 0.15)
            elif char in '@._-':
                # Slower for special characters in emails
                delay = random.uniform(0.1, 0.2)
            else:
                # Normal speed for other characters
                delay = random.uniform(0.05, 0.12)
            
            # Add occasional longer pauses (thinking)
            if random.random() < 0.05:
                delay += random.uniform(0.3, 0.8)
            
            time.sleep(delay)
            i += 1
        
        logger.info(f"Successfully typed text of length {len(text)}")
    except Exception as e:
        logger.error(f"Error during human_type: {str(e)}")
        raise


def human_click(page, element):
    """Simulate human-like clicking with slight movement"""
    logger.info("Starting human_click")
    
    try:
        # Get element bounding box for realistic clicking
        bbox = element.bounding_box()
        if bbox:
            # Click at a random position within the element (not always center)
            x = bbox['x'] + random.uniform(0.2, 0.8) * bbox['width']
            y = bbox['y'] + random.uniform(0.2, 0.8) * bbox['height']
            
            logger.debug(f"Element bbox found, clicking at coordinates ({x:.1f}, {y:.1f})")
            
            # Move mouse to position with some randomness
            page.mouse.move(x + random.uniform(-2, 2), y + random.uniform(-2, 2))
            time.sleep(random.uniform(0.1, 0.3))
            
            # Click
            page.mouse.click(x, y)
            logger.debug("Mouse click completed")
        else:
            logger.warning("Element bbox not found, using fallback click")
            # Fallback to regular click
            element.click()
        
        logger.info("Successfully completed human_click")
    except Exception as e:
        logger.error(f"Error during human_click: {str(e)}")
        raise