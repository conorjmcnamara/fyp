import React, { useState } from 'react';
import { FiUpload } from 'react-icons/fi'; // Import the upload icon from react-icons
import { PaperResponse, uploadPdf } from '../../services/recommendationService';

interface UploadPdfProps {
  numRecommendations: number;
  onResults: (papers: PaperResponse[]) => void;
}

const UploadPdf: React.FC<UploadPdfProps> = ({ onResults, numRecommendations }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);
  const [uploadComplete, setUploadComplete] = useState<boolean>(false);

  // Reset state when a new file is selected
  const resetState = () => {
    setError(null);
    setFileName(null);
    setUploadComplete(false);
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    resetState(); // Reset state when a new file is selected

    const maxSize = 5 * 1024 * 1024; // 50 MB
    if (file.size > maxSize) {
      setError('File size exceeds the 50 MB limit');
      setLoading(false);
      return; // Stop further processing if the file is too large
    }

    if (file.type !== "application/pdf") {
      setError('Invalid file type. Please upload a PDF file.');
      return;
    }

    setFileName(file.name);
    setLoading(true);

    try {
      const data = await uploadPdf(file, numRecommendations);
      setUploadComplete(true);
      onResults(data.papers);
    } catch (error: unknown) {
      const errorMsg = error instanceof Error
        ? `Failed to upload PDF: ${error.message}`
        : 'Failed to upload PDF';
      setError(errorMsg);
    } finally {
      setLoading(false);
      e.target.value = "";
    }
  };

  return (
    <div>
      <h2 className="text-xl font-semibold mb-1">Upload your PDF</h2>
      <p className="text-gray-500 mb-4">
        Drag and drop your PDF, or click to select a file.
      </p>

      {/* New Dropzone UI */}
      <div className="flex items-center justify-center w-full">
        <label
          htmlFor="dropzone-file"
          className="flex flex-col items-center justify-center w-full h-60 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 dark:hover:bg-gray-800 dark:bg-gray-700 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600"
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            {loading ? (
              <div className="animate-spin inline-block w-10 h-10 border-[3px] border-t-transparent border-gray-200 rounded-full mb-4" />
            ) : (
              <>
                <FiUpload className="w-8 h-8 mb-3 text-gray-500 dark:text-gray-400" />
                <p className="mb-1 text-lg text-gray-500 dark:text-gray-400">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Pick a PDF up to 5 MB.
                </p>
              </>
            )}
          </div>
          <input
            id="dropzone-file"
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="hidden"
          />
        </label>
      </div>

      {/* Display File Name and Upload Status */}
      {fileName && !loading && !error && (
        <div className="mt-4 text-gray-700">
          <p className="font-semibold truncate max-w-full">
            {fileName}
          </p>
          {uploadComplete && <p className="text-sm text-gray-500">Upload complete</p>}
        </div>
      )}

      {error && <p className="text-red-600 text-sm font-medium mt-4">{error}</p>}
    </div>
  );
};

export default UploadPdf;
