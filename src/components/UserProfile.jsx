import React, { useState, useEffect } from 'react';
import { themeService } from '../services/themeService';

const UserProfile = ({ userId }) => {
  const [theme, setTheme] = useState('light');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load saved theme on mount
    const savedTheme = themeService.getTheme(userId);
    setTheme(savedTheme);
    themeService.applyTheme(savedTheme);
  }, [userId]);

  const handleThemeToggle = async () => {
    setLoading(true);
    try {
      const newTheme = theme === 'light' ? 'dark' : 'light';
      await themeService.saveTheme(userId, newTheme);
      setTheme(newTheme);
      themeService.applyTheme(newTheme);
    } catch (error) {
      console.error('Failed to update theme:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="user-profile">
      <h2>User Profile</h2>
      <div className="theme-toggle-container">
        <label htmlFor="theme-toggle">Theme:</label>
        <button
          id="theme-toggle"
          onClick={handleThemeToggle}
          disabled={loading}
          className={`theme-toggle-btn ${theme}`}
        >
          {loading ? 'Switching...' : theme === 'light' ? '🌞 Light' : '🌙 Dark'}
        </button>
      </div>
    </div>
  );
};

export default UserProfile;
