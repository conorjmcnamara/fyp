import React, { useState } from 'react';
import Header from '../../components/Header/Header';
import SearchForm from '../../components/SearchForm/SearchForm';
import Results from '../../components/RecommendationResults/RecommendationResults';
import { PaperResponse } from '../../services/recommendationService';

const HomePage: React.FC = () => {
  const [papers, setPapers] = useState<PaperResponse[]>([]);

  const handleResults = (newPapers: PaperResponse[]) => {
    setPapers(newPapers);
  };

  return (
    <div className="max-w-full sm:max-w-2xl mx-auto p-6">
      <div className="bg-white p-5 rounded-lg shadow-lg">
        <Header />
      </div>

      <div className="bg-white p-6 mt-10 rounded-lg shadow-lg">
        <SearchForm onResults={handleResults} />
      </div>

      {papers.length > 0 && (
        <div className="bg-white p-6 mt-10 rounded-lg shadow-lg">
          <Results papers={papers} />
        </div>
      )}
    </div>
  );
};

export default HomePage;
