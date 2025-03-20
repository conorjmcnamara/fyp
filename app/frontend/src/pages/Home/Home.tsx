import React, { useState } from 'react';
import Header from '../../components/Header/Header';
import TabToggle from '../../components/TabToggle/TabToggle';
import Results from '../../components/RecommendationResults/RecommendationResults';
import { PaperResponse } from '../../services/recommendationService';

const Home: React.FC = () => {
  const [papers, setPapers] = useState<PaperResponse[]>([]);

  const handleResults = (newPapers: PaperResponse[]) => {
    setPapers(newPapers);
  };

  return (
    <div className="max-w-full sm:max-w-3xl mx-auto p-6">
      <div className="card">
        <Header />
      </div>

      <div className="card mt-10">
        <TabToggle onResults={handleResults} />
      </div>

      {papers.length > 0 && (
        <div className="card mt-10">
          <Results papers={papers} />
        </div>
      )}
    </div>
  );
};

export default Home;
