const THEME_STORAGE_KEY = 'user_theme_preference';

export const themeService = {
  /**
   * Get theme preference from localStorage
   */
  getTheme(userId) {
    try {
      const stored = localStorage.getItem(`${THEME_STORAGE_KEY}_${userId}`);
      return stored || 'light';
    } catch (error) {
      console.error('Error reading theme:', error);
      return 'light';
    }
  },

  /**
   * Save theme preference to localStorage and backend
   */
  async saveTheme(userId, theme) {
    if (!userId) {
      throw new Error('User ID is required');
    }

    if (!['light', 'dark', 'auto'].includes(theme)) {
      throw new Error('Invalid theme option');
    }

    try {
      // Save to localStorage
      localStorage.setItem(`${THEME_STORAGE_KEY}_${userId}`, theme);

      // Save to backend
      const response = await fetch(`/api/users/${userId}/preferences`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ theme }),
      });

      if (!response.ok) {
        throw new Error('Failed to save theme preference');
      }

      return theme;
    } catch (error) {
      console.error('Error saving theme:', error);
      throw error;
    }
  },

  /**
   * Apply theme to document
   */
  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
  },

  /**
   * Clear theme preference
   */
  clearTheme(userId) {
    localStorage.removeItem(`${THEME_STORAGE_KEY}_${userId}`);
  }
};
