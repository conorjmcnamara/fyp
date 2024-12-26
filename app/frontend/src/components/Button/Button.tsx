import React, { useState } from 'react';
import { fetchMessage } from '../../services/messageService';
import styles from './Button.module.css'

const Button: React.FC = () => {
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleClick = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await fetchMessage();
      setMessage(data.message);
    } catch (err) {
      setError('Failed to fetch message.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.buttonContainer}>
      <button onClick={handleClick} className={styles.button}>
        Get Message
      </button>
      {loading && <p>Loading...</p>}
      {error && <p className={styles.error}>{error}</p>}
      {message && <p className={styles.message}>{message}</p>}
    </div>
  );
};

export default Button;
