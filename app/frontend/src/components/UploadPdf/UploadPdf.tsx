import React, { useState } from 'react';
import { FiUpload } from 'react-icons/fi';
import { MAX_FILE_SIZE_BYTES } from '../../config/config';
import { PaperResponse, uploadPdf } from '../../services/recommendationService';
import styles from './UploadPdf.module.css';

interface UploadPdfProps {
  numRecommendations: number;
  onResults: (papers: PaperResponse[]) => void;
}

const UploadPdf: React.FC<UploadPdfProps> = ({ onResults, numRecommendations }) => {
  const [uploadComplete, setUploadComplete] = useState<boolean>(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadComplete(false);
    setFileName(file.name);

    if (file.type !== "application/pdf") {
      setError('Invalid file type. Please upload a PDF file.');
      return;
    }
    
    if (file.size > MAX_FILE_SIZE_BYTES) {
      setError(`File size must not exceed the ${MAX_FILE_SIZE_BYTES / 1024 / 1024} MB limit.`);
      return;
    }

    setError(null);
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
        Drag and drop your research manuscript as a PDF, or click to upload.
      </p>

      <div>
        <label htmlFor="dropzone" className={styles.dropzone}>
          <div className="flex flex-col items-center justify-center pt-5 pb-5">
            {loading ? (
              <div className="spinner size-12" />
            ) : (
              <>
                <FiUpload className="w-8 h-8 mb-3 text-gray-500" />
                <p className="mb-1 text-lg text-gray-500">
                  <span className="font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-sm text-gray-500">
                  Pick a PDF up to {MAX_FILE_SIZE_BYTES / 1024 / 1024} MB.
                </p>
              </>
            )}
          </div>
          <input
            id="dropzone"
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="hidden"
          />
        </label>
      </div>

      <div className="mt-4">
        {fileName && !loading && (
          <div>
            <p className="font-semibold text-gray-700">{fileName}</p>
            {uploadComplete && <p className="text-sm text-gray-500">Upload complete.</p>}
          </div>
        )}

        {error && <p className="text-red-600 font-medium">{error}</p>}
      </div>
    </div>
  );
};

export default UploadPdf;
