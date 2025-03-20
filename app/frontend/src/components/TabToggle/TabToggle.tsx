import React, { useState } from 'react';
import { FaSearch, FaFileUpload } from 'react-icons/fa';
import SearchForm from '../SearchForm/SearchForm';
import UploadPdf from '../UploadPdf/UploadPdf';
import { PaperResponse } from '../../services/recommendationService';
import styles from './TabToggle.module.css';

interface TabToggleProps {
  onResults: (papers: PaperResponse[]) => void;
}

const TabToggle: React.FC<TabToggleProps> = ({ onResults }) => {
  const [selectedTab, setSelectedTab] = useState<'search' | 'pdf'>('search');
  const [numRecommendations, setNumRecommendations] = useState<number>(10);

  return (
    <div>
      {/* Tab toggle - Inline on desktop, stacked on mobile */}
      <div className="flex flex-col sm:flex-row gap-2 sm:gap-0 mb-5">
        <button
          className={`${styles.tabButton} ${
            selectedTab === 'search'
              ? styles.activeTab
              : `${styles.inactiveTab} ${styles.inactiveTabHover}`
          }`}
          onClick={() => setSelectedTab('search')}
        >
          <FaSearch className="inline mr-2" />
          Search by Title/Abstract
        </button>

        <button
          className={`${styles.tabButton} ${
            selectedTab === 'pdf'
              ? styles.activeTab
              : `${styles.inactiveTab} ${styles.inactiveTabHover}`
          }`}
          onClick={() => setSelectedTab('pdf')}
        >
          <FaFileUpload className="inline mr-2" />
          Upload PDF
        </button>
      </div>

      {/* Number of Recommendations dropdown */}
      <div className="mb-5">
        <label htmlFor="numRecommendations" className="block text-sm font-medium text-gray-700">
          Number of Recommendations
        </label>
        <select
          id="numRecommendations"
          value={numRecommendations}
          onChange={(e) => setNumRecommendations(Number(e.target.value))}
          className="w-full p-2 border border-gray-300 rounded-lg"
        >
          <option value={10}>10</option>
          <option value={25}>25</option>
          <option value={50}>50</option>
        </select>
      </div>

      {/* Tab content */}
      <div>
        {selectedTab === 'search' ? (
          <SearchForm numRecommendations={numRecommendations} onResults={onResults} />
        ) : (
          <UploadPdf numRecommendations={numRecommendations} onResults={onResults} />
        )}
      </div>
    </div>
  );
};

export default TabToggle;
