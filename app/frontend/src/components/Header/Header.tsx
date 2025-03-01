import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="text-center">
      <h1 className="text-3xl font-semibold">Citation Recommender</h1>
      <p className="text-lg text-gray-500 mt-2">Find relevant citations for your research</p>
    </header>
  );
};

export default Header;
