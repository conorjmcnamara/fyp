import React, { useState } from 'react';
import { MAX_TEXT_LENGTH } from '../../config/config';
import { fetchRecommendations, PaperResponse } from '../../services/recommendationService';
import styles from './SearchForm.module.css';

interface SearchFormProps {
  onResults: (papers: PaperResponse[]) => void;
  numRecommendations: number;
  maxTextLength?: number;
}

const SearchForm: React.FC<SearchFormProps> = (
  { onResults, numRecommendations, maxTextLength = MAX_TEXT_LENGTH }
) => {
  const [title, setTitle] = useState<string>('');
  const [abstract, setAbstract] = useState<string>('');
  const [isTooLong, setIsTooLong] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const validateTextLength = (title: string, abstract: string): boolean => {
    return (title + abstract).length <= maxTextLength;
  };

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTitle = e.target.value;
    setTitle(newTitle);

    const validLength = validateTextLength(newTitle, abstract);
    setIsTooLong(!validLength);
    setError(
      validLength
        ? null
        : `Title and abstract must not exceed ${maxTextLength} characters.`
    );
  };

  const handleAbstractChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newAbstract = e.target.value;
    setAbstract(newAbstract);

    const validLength = validateTextLength(title, newAbstract);
    setIsTooLong(!validLength);
    setError(
      validLength
        ? null
        : `Title and abstract must not exceed ${maxTextLength} characters.`
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title && !abstract) {
      setError('A title, an abstract, or both must be provided.');
      return;
    }

    if (isTooLong) return;

    setError(null);
    setLoading(true);
    
    try {
      const data = await fetchRecommendations(title, abstract, numRecommendations);
      onResults(data.papers);
    } catch (error: unknown) {
      const errorMsg = error instanceof Error
        ? `Failed to fetch recommendations: ${error.message}`
        : 'Failed to fetch recommendations';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="text-xl font-semibold mb-1">Search Form</h2>
      <p className="text-gray-500 mb-4">
        Enter the title and/or abstract of your research.
      </p>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label htmlFor="title" className={styles.label}>Title</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={handleTitleChange}
            className={styles.input}
          />
        </div>

        <div>
          <label htmlFor="abstract" className={styles.label}>Abstract</label>
          <textarea
            id="abstract"
            value={abstract}
            onChange={handleAbstractChange}
            className={styles.input}
            rows={4}
          />
        </div>

        {error && <p className="text-red-600 font-medium">{error}</p>}

        <button 
          type="submit" 
          className="
            w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 flex justify-center
            items-center
          "
        >
          {loading ? <div className="spinner size-6" /> : 'Search'}
        </button>
      </form>
    </div>
  );
};

export default SearchForm;
