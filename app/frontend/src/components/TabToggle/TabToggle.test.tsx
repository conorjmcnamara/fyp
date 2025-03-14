import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TabToggle from './TabToggle';
import SearchForm from '../SearchForm/SearchForm';
import UploadPdf from '../UploadPdf/UploadPdf';
import { PaperResponse } from '../../services/recommendationService';

jest.mock('../SearchForm/SearchForm', () => ({
  __esModule: true,
  default: jest.fn()
}));
const searchFormMock = SearchForm as jest.Mock;

jest.mock('../UploadPdf/UploadPdf', () => ({
  __esModule: true,
  default: jest.fn()
}));
const uploadPdfMock = UploadPdf as jest.Mock;

const mockPapers: PaperResponse[] = [
  {
    id: '1',
    title: 'Paper 1',
    year: 2025,
    abstract: 'Abstract for paper 1',
    venue: 'Venue 1',
    authors: [{ first_name: 'John', last_name: 'Doe' }],
    recommendation_score: 95
  }
];

describe('TabToggle', () => {
  it('should toggle the active tab', () => {
    searchFormMock.mockReturnValue(<div>SearchForm component</div>);
    uploadPdfMock.mockReturnValue(<div>UploadPdf component</div>);

    render(<TabToggle onResults={jest.fn()} />);

    const searchTab = screen.getByText(/Search by Title\/Abstract/i);
    const uploadTab = screen.getByText(/Upload PDF/i);

    expect(searchTab).toBeInTheDocument();
    expect(uploadTab).toBeInTheDocument();

    expect(searchTab).toHaveClass('activeTab');
    expect(uploadTab).not.toHaveClass('activeTab');
    expect(screen.getByText(/SearchForm component/i)).toBeInTheDocument();
    expect(screen.queryByText(/UploadPdf component/i)).not.toBeInTheDocument();

    fireEvent.click(screen.getByText(/Upload PDF/i));
    expect(searchTab).not.toHaveClass('activeTab');
    expect(uploadTab).toHaveClass('activeTab');
    expect(screen.queryByText(/SearchForm component/i)).not.toBeInTheDocument();
    expect(screen.getByText(/UploadPdf component/i)).toBeInTheDocument();

    fireEvent.click(screen.getByText(/Search by Title\/Abstract/i));
    expect(searchTab).toHaveClass('activeTab');
    expect(uploadTab).not.toHaveClass('activeTab');
    expect(screen.getByText(/SearchForm component/i)).toBeInTheDocument();
    expect(screen.queryByText(/UploadPdf component/i)).not.toBeInTheDocument();
  });

  it('should render the dropdown with the correct number of recommendations options', () => {
    render(<TabToggle onResults={jest.fn()} />);

    const dropdown = screen.getByLabelText(/Number of Recommendations/i);
    expect(dropdown).toBeInTheDocument();

    expect(dropdown).toHaveTextContent('10');
    expect(dropdown).toHaveTextContent('25');
    expect(dropdown).toHaveTextContent('50');
    
    const options = screen.getAllByRole('option');
    expect(options).toHaveLength(3);
  });

  it('should update numRecommendations on selection change', () => {
    render(<TabToggle onResults={jest.fn()} />);

    const dropdown = screen.getByLabelText(/Number of Recommendations/i) as HTMLSelectElement;
    expect(dropdown.value).toBe('10');

    fireEvent.change(dropdown, { target: { value: '25' } });
    expect(dropdown.value).toBe('25');

    fireEvent.change(dropdown, { target: { value: '100' } });
    expect(dropdown).not.toHaveValue('100');
  });

  it('should pass numRecommendations prop to the SearchForm component', () => {
    render(<TabToggle onResults={jest.fn()} />);

    expect(SearchForm).toHaveBeenCalledWith(
      expect.objectContaining({
        numRecommendations: 10,
      }),
      expect.anything()
    );

    const dropdown = screen.getByLabelText(/Number of Recommendations/i);
    fireEvent.change(dropdown, { target: { value: '25' } });

    expect(SearchForm).toHaveBeenCalledWith(
      expect.objectContaining({
        numRecommendations: 25,
      }),
      expect.anything()
    );
  });

  it('should pass numRecommendations prop to the UploadPdf component', () => {
    render(<TabToggle onResults={jest.fn()} />);
    fireEvent.click(screen.getByText(/Upload PDF/i));
    
    expect(UploadPdf).toHaveBeenCalledWith(
      expect.objectContaining({
        numRecommendations: 10,
      }),
      expect.anything()
    );

    const dropdown = screen.getByLabelText(/Number of Recommendations/i);
    fireEvent.change(dropdown, { target: { value: '25' } });

    expect(UploadPdf).toHaveBeenCalledWith(
      expect.objectContaining({
        numRecommendations: 25,
      }),
      expect.anything()
    );
  });

  it('should call onResults when the SearchForm component triggers results', async () => {
    searchFormMock.mockImplementation(
      ({ onResults }: { onResults: (papers: PaperResponse[]) => void }) => (
        <div>
          <button onClick={() => onResults(mockPapers)}>Trigger results</button>
        </div>
      )
    );

    const onResultsMock = jest.fn();
    render(<TabToggle onResults={onResultsMock} />);

    fireEvent.click(screen.getByText(/Trigger results/i));
    await waitFor(() => {
      expect(onResultsMock).toHaveBeenCalledWith(mockPapers);
    });
  });

  it('should call onResults when the UploadPdf component triggers results', async () => {
    uploadPdfMock.mockImplementation(
      ({ onResults }: { onResults: (papers: PaperResponse[]) => void }) => (
        <div>
          <button onClick={() => onResults(mockPapers)}>Trigger results</button>
        </div>
      )
    );

    const onResultsMock = jest.fn();
    render(<TabToggle onResults={onResultsMock} />);

    fireEvent.click(screen.getByText(/Upload PDF/i));
    fireEvent.click(screen.getByText(/Trigger results/i));
    await waitFor(() => {
      expect(onResultsMock).toHaveBeenCalledWith(mockPapers);
    });
  });
});
