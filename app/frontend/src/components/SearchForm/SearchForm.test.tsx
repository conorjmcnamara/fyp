import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { fetchRecommendations } from '../../services/recommendationService';
import SearchForm from './SearchForm';

jest.mock('../../services/recommendationService', () => ({
  fetchRecommendations: jest.fn(),
}));

describe('SearchForm', () => {
  it('renders the form with title and abstract inputs and a search button', () => {
    render(<SearchForm onResults={jest.fn()} />);

    expect(screen.getByLabelText(/Title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Abstract/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Search/i })).toBeInTheDocument();
  });

  it('shows an error when both title and abstract are empty', async () => {
    render(<SearchForm onResults={jest.fn()} />);

    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    expect(
      await screen.findByText(/Either title or abstract must be provided./i)
    ).toBeInTheDocument();
  });

  it('does not show an error when title is provided but abstract is empty', async () => {
    render(<SearchForm onResults={jest.fn()} />);
  
    fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'Some title' } });
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    await waitFor(() => expect(
      screen.queryByText(/Either title or abstract must be provided./i)
    ).not.toBeInTheDocument());
  });
  
  it('does not show an error when abstract is provided but title is empty', async () => {
    render(<SearchForm onResults={jest.fn()} />);
  
    fireEvent.change(screen.getByLabelText(/Abstract/i), { target: { value: 'Some abstract' } });
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));
  
    await waitFor(() => expect(
      screen.queryByText(/Either title or abstract must be provided./i)
    ).not.toBeInTheDocument());
  });

  it('does not show an error when title or abstract is provided', async () => {
    render(<SearchForm onResults={jest.fn()} />);
  
    fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'Some title' } });
    fireEvent.change(screen.getByLabelText(/Abstract/i), { target: { value: 'Some abstract' } });
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));
  
    await waitFor(() => expect(
      screen.queryByText(/Either title or abstract must be provided./i)
    ).not.toBeInTheDocument());
  });
  
  it('calls onResults when recommendations are fetched successfully', async () => {
    const mockOnResults = jest.fn();
    const mockPapers = [{ title: 'Paper 1' }];
    (fetchRecommendations as jest.Mock).mockResolvedValue({ papers: mockPapers });

    render(<SearchForm onResults={mockOnResults} />);

    fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'Some title' } });
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    await waitFor(() => expect(mockOnResults).toHaveBeenCalledWith(mockPapers));
  });

  it('shows an error message when fetchRecommendations fails', async () => {
    const mockOnResults = jest.fn();
    (fetchRecommendations as jest.Mock).mockRejectedValue(new Error('Network Error'));

    render(<SearchForm onResults={mockOnResults} />);

    fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'Some title' } });
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    expect(
      await screen.findByText(/Failed to fetch recommendations: Network Error/i)
    ).toBeInTheDocument();
  });

  it(
    'shows a generic error message when fetchRecommendations fails with a non-Error value',
    async () => {
      const mockOnResults = jest.fn();
      (fetchRecommendations as jest.Mock).mockRejectedValue('Network Error');
  
      render(<SearchForm onResults={mockOnResults} />);
  
      fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'Some title' } });
      fireEvent.click(screen.getByRole('button', { name: /Search/i }));
  
      expect(await screen.findByText(/Failed to fetch recommendations/i)).toBeInTheDocument();
    }
  );
});
