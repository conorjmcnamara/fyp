import React, { useState } from 'react';
import { fetchRecommendations, PaperResponse } from '../../services/recommendationService';

interface SearchFormProps {
  onResults: (papers: PaperResponse[]) => void;
}

const SearchForm: React.FC<SearchFormProps> = ({ onResults }) => {
  const [title, setTitle] = useState<string>('');
  const [abstract, setAbstract] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async(e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!title && !abstract) {
      setError('Either title or abstract must be provided.');
      return;
    }

    setLoading(true);
    try {
      const data = await fetchRecommendations(title, abstract);
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
        Enter the title or abstract of your research to find relevant citations.
      </p>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">Title</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="
              w-full p-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500
            "
          />
        </div>

        <div>
          <label htmlFor="abstract" className="block text-sm font-medium text-gray-700">
            Abstract
          </label>
          <textarea
            id="abstract"
            value={abstract}
            onChange={(e) => setAbstract(e.target.value)}
            className="
              w-full p-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500
            "
            rows={4}
          />
        </div>

        {error && (
          <p className="text-red-600 text-sm font-medium">{error}</p>
        )}

        <button 
          type="submit" 
          className="
            w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 flex justify-center
            items-center
          "
        >
          {loading ? (
            <div
              className="
                animate-spin inline-block size-6 border-[3px] border-t-transparent border-gray-200
                rounded-full
              "
            />
          ) : (
            'Search'
          )}
        </button>
      </form>
    </div>
  )
};

export default SearchForm;