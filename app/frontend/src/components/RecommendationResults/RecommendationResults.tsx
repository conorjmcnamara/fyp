import React, { useState } from 'react';
import { PaperResponse } from '../../services/recommendationService';

interface RecommendationResultsProps {
  papers: PaperResponse[];
  papersPerPage?: number;
}

const RecommendationResults: React.FC<RecommendationResultsProps> = (
  { papers, papersPerPage = 5 }
) => {
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [expandedPaperId, setExpandedPaperId] = useState<string | null>(null);
  
  const indexOfLastPaper = currentPage * papersPerPage;
  const indexOfFirstPaper = indexOfLastPaper - papersPerPage;
  const currentPapers = papers.slice(indexOfFirstPaper, indexOfLastPaper);

  const goToNextPage = () => {
    setCurrentPage(currentPage + 1);
  };

  const goToPrevPage = () => {
    setCurrentPage(currentPage - 1);
  };

  const toggleExpandedPaper = (id: string) => {
    setExpandedPaperId(expandedPaperId === id ? null : id);
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-6">Recommended Citations</h2>

      {/* Pagination controls */}
      <div className="flex justify-center space-x-2 mb-4">
        {currentPage > 1 && (
          <button
            className="px-3 py-1 bg-gray-300 rounded-lg hover:bg-gray-400"
            onClick={goToPrevPage}
          >
            Prev
          </button>
        )}

        <span className="px-3 py-1 bg-blue-500 text-white rounded-lg">
          {currentPage}
        </span>

        {currentPage * papersPerPage < papers.length && (
          <button
            className="px-3 py-1 bg-gray-300 rounded-lg hover:bg-gray-400"
            onClick={goToNextPage}
          >
            Next
          </button>
        )}
      </div>

      {/* Papers list */}
      <div className="space-y-6">
        {currentPapers.map((paper) => (
          <div key={paper.id} className="p-6 bg-white shadow-md rounded-lg">
            <h3 className="text-2xl font-bold mb-2">{paper.title} ({paper.year})</h3>

            <div className="mb-4">
              <span className="text-gray-700">Recommendation Score:</span>
              <span className="ml-2 text-lg font-semibold text-green-500">
                {paper.recommendation_score.toFixed(2)}
              </span>
            </div>

            <div className="text-sm text-gray-600 mb-4">
              {paper.authors.map((author, index) => (
                <span key={index}>
                  {author.first_name} {author.last_name}
                  {index < paper.authors.length - 1 && ', '}
                </span>
              ))}
            </div>
          
            <div className="text-sm text-gray-500 mb-4">{paper.venue}</div>
         
            <div>
              {expandedPaperId === paper.id ? (
                <div>
                  <p className="text-sm text-gray-700 mt-2">{paper.abstract}</p>
                  <button
                    onClick={() => toggleExpandedPaper(paper.id)}
                    className="text-sm text-red-500 hover:text-red-700 mt-2"
                  >
                    Hide Abstract
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => toggleExpandedPaper(paper.id)}
                  className="flex items-center text-sm text-blue-500 hover:text-blue-700 mt-2"
                >
                  View Abstract
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationResults;
