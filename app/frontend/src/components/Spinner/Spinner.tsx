import React from 'react';

const Spinner: React.FC = () => {
  return (
    <div
      className="
        animate-spin inline-block size-6 border-[3px] border-t-transparent border-gray-200
        rounded-full
      "
    />
  )
};

export default Spinner;
