import React, { useState } from 'react';
import { HiChevronDown, HiChevronUp } from 'react-icons/hi';
import flowImage from '../../assets/images/recommendation_flow.png';

const Header: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  return (
    <header className="text-center">
      <h1 className="text-3xl font-semibold">Citation Recommender</h1>
      <p className="text-lg text-gray-500 mt-2">Find relevant citations for your research</p>

      <div className="mt-3">
        <div className="flex justify-center">
          <button
            className="flex items-center gap-2 font-medium text-blue-500 hover:text-blue-700"
            onClick={() => setIsOpen(!isOpen)}
          >
            <span>How does it work?</span>
            {isOpen ? <HiChevronUp size={20} /> : <HiChevronDown size={20} />}
          </button>
        </div>

        <div
          className={`
            overflow-hidden transition-all duration-300 ease-in-out 
            ${isOpen ? 'max-h-[1000px]' : 'max-h-0'}
          `}
        >
          <div className="p-4 border mt-3 rounded-lg bg-gray-50">
            <img src={flowImage} alt="Recommendation flow diagram" className="w-[80%] mx-auto" />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
