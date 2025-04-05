import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { uploadPdf } from '../../services/recommendationService';
import { MAX_FILE_SIZE_BYTES } from '../../config/config';
import UploadPdf from './UploadPdf';

jest.mock('../../services/recommendationService', () => ({
  uploadPdf: jest.fn(),
}));

describe('UploadPdf', () => {
  const numRecommendations = 5;
  const file = new File(['Example text'], 'example.pdf', { type: 'application/pdf' });

  it('renders the component with file input and instructions', () => {
    render(<UploadPdf onResults={jest.fn()} numRecommendations={numRecommendations} />);

    expect(screen.getByLabelText(/Click to upload/i)).toBeInTheDocument();
    expect(
      screen.getByText(/Drag and drop your research manuscript as a PDF, or click to upload./i)
    ).toBeInTheDocument();
  });

  it('displays an error when a non-PDF file is uploaded', async () => {
    const invalidFile = new File(['Example text'], 'example.txt', { type: 'text/plain' });
    render(<UploadPdf onResults={jest.fn()} numRecommendations={numRecommendations} />);

    const input = screen.getByLabelText(/Click to upload/i);
    fireEvent.change(input, { target: { files: [invalidFile] } });
    
    expect(
      await screen.findByText(/Invalid file type. Please upload a PDF file./i)
    ).toBeInTheDocument();
  });

  it('displays an error when the file size exceeds the limit', async () => {
    const largeFile = new File([new ArrayBuffer(MAX_FILE_SIZE_BYTES + 1)], 'large.pdf', {
      type: 'application/pdf',
    });
    render(<UploadPdf onResults={jest.fn()} numRecommendations={numRecommendations} />);

    const input = screen.getByLabelText(/Click to upload/i);
    fireEvent.change(input, { target: { files: [largeFile] } });

    expect(
      await screen.findByText(
        new RegExp(`File size exceeds the ${MAX_FILE_SIZE_BYTES / 1024 / 1024} MB limit`, 'i')
      )
    ).toBeInTheDocument();
  });

  it('resets the input value after a file upload attempt', async () => {
    (uploadPdf as jest.Mock).mockResolvedValue({ papers: [] });
    render(<UploadPdf onResults={jest.fn()} numRecommendations={numRecommendations} />);

    const input = screen.getByLabelText(/Click to upload/i) as HTMLInputElement;
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => expect(input.value).toBe(''));
  });

  it('calls onResults when uploadPdf is called on valid input', async () => {
    const mockOnResults = jest.fn();
    const mockPapers = [{ title: 'Paper 1' }];

    (uploadPdf as jest.Mock).mockResolvedValue({ papers: mockPapers });
    render(<UploadPdf onResults={mockOnResults} numRecommendations={numRecommendations} />);

    const input = screen.getByLabelText(/Click to upload/i);
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => expect(uploadPdf).toHaveBeenCalledWith(file, numRecommendations));
    await waitFor(() => expect(mockOnResults).toHaveBeenCalledWith(mockPapers));
  });

  it('does not call uploadPdf when no file is selected', async () => {
    render(<UploadPdf onResults={jest.fn()} numRecommendations={numRecommendations} />);
    
    const input = screen.getByLabelText(/Click to upload/i);
    fireEvent.change(input, { target: { files: [] } });

    await waitFor(() => expect(uploadPdf).not.toHaveBeenCalled());
  });

  it('displays an error when uploadPdf fails', async () => {
    (uploadPdf as jest.Mock).mockRejectedValue(new Error('Network Error'));
    render(<UploadPdf onResults={jest.fn()} numRecommendations={numRecommendations} />);

    const input = screen.getByLabelText(/Click to upload/i);
    fireEvent.change(input, { target: { files: [file] } });

    expect(
      await screen.findByText(/Failed to upload PDF: Network Error/i)
    ).toBeInTheDocument();
  });

  it('displays a generic error when uploadPdf fails with a non-Error type', async () => {
    (uploadPdf as jest.Mock).mockRejectedValue('Unknown error');
    render(<UploadPdf onResults={jest.fn()} numRecommendations={numRecommendations} />);

    const input = screen.getByLabelText(/Click to upload/i);
    fireEvent.change(input, { target: { files: [file] } });

    expect(await screen.findByText(/Failed to upload PDF/i)).toBeInTheDocument();
  });
});
