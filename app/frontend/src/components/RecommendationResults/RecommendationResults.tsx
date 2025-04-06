import React, { useState, useEffect } from 'react';
import { PAPERS_PER_PAGE } from '../../config/config';
import { PaperResponse } from '../../services/recommendationService';
import styles from './RecommendationResults.module.css';

interface RecommendationResultsProps {
  papers: PaperResponse[];
  papersPerPage?: number;
}

const RecommendationResults: React.FC<RecommendationResultsProps> = (
  { papers, papersPerPage = PAPERS_PER_PAGE }
) => {
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [expandedPaperId, setExpandedPaperId] = useState<string | null>(null);

  useEffect(() => {
    setCurrentPage(1);
    setExpandedPaperId(null);
  }, [papers]);
  
  const indexOfLastPaper = currentPage * papersPerPage;
  const indexOfFirstPaper = indexOfLastPaper - papersPerPage;
  const currentPapers = papers.slice(indexOfFirstPaper, indexOfLastPaper);

  const goToNextPage = () => setCurrentPage((prev) => prev + 1);
  const goToPrevPage = () => setCurrentPage((prev) => prev - 1);
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
            className={styles.paginationButton}
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
            className={styles.paginationButton}
            onClick={goToNextPage}
          >
            Next
          </button>
        )}
      </div>

      {/* Papers list */}
      <div className="space-y-6">
        {currentPapers.map((paper) => (
          <div key={paper.id} className="card">
            <h3 className="text-2xl font-bold mb-2">{paper.title} ({paper.year})</h3>

            <div className="mb-4">
              <span className="text-gray-700">Recommendation Score:</span>
              <span className="ml-2 text-lg font-semibold text-green-500">
                {paper.recommendation_score.toFixed(3)}
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
                    className="text-sm font-bold text-red-500 hover:text-red-600 mt-2"
                  >
                    Hide Abstract
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => toggleExpandedPaper(paper.id)}
                  className="text-sm font-bold text-blue-500 hover:text-blue-600 mt-2"
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
