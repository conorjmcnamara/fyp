import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { fetchRecommendations } from '../../services/recommendationService';
import SearchForm from './SearchForm';

jest.mock('../../services/recommendationService', () => ({
  fetchRecommendations: jest.fn(),
}));

describe('SearchForm', () => {
  const numRecommendations = 5;

  it('renders the component with input fields, a search button, and instructions', () => {
    render(<SearchForm onResults={jest.fn()} numRecommendations={numRecommendations} />);

    expect(screen.getByLabelText(/Title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Abstract/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Search/i })).toBeInTheDocument();
    expect(
      screen.getByText(/Enter the title and\/or abstract of your research/i)
    ).toBeInTheDocument();
  });

  describe('field presence', () => {
    it('displays an error when both fields are empty on submit', () => {
      render(<SearchForm onResults={jest.fn()} numRecommendations={numRecommendations} />);
  
      fireEvent.click(screen.getByRole('button', { name: /Search/i }));
      expect(
        screen.getByText(/A title, an abstract, or both must be provided./i)
      ).toBeInTheDocument();
    });
  
    it('does not display an error when title is provided but abstract is empty', async () => {
      render(<SearchForm onResults={jest.fn()} numRecommendations={numRecommendations} />);
  
      fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'Example title' } });
      fireEvent.click(screen.getByRole('button', { name: /Search/i }));
  
      await waitFor(() => expect(
        screen.queryByText(/Either title or abstract must be provided./i)
      ).not.toBeInTheDocument());
    });
  
    it('does not display an error when abstract is provided but title is empty', async () => {
      render(<SearchForm onResults={jest.fn()} numRecommendations={numRecommendations} />);
  
      fireEvent.change(screen.getByLabelText(/Abstract/i), { target: { value: 'Example abstract' } });
      fireEvent.click(screen.getByRole('button', { name: /Search/i }));
  
      await waitFor(() => expect(
        screen.queryByText(/Either title or abstract must be provided./i)
      ).not.toBeInTheDocument());
    });
  });

  describe('max text length', () => {
    const maxTextLength = 20;
    const maxTextLengthErrorMsg = `Title and abstract must not exceed ${maxTextLength} characters.`;

    it('does not display an error when title length has max length', () => {
      render(
        <SearchForm
          onResults={jest.fn()}
          numRecommendations={numRecommendations}
          maxTextLength={maxTextLength}
        />
      );

      fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'A'.repeat(maxTextLength) } });
      expect(screen.queryByText(new RegExp(maxTextLengthErrorMsg, 'i'))).not.toBeInTheDocument();
    });

    it('displays an error when title length exceeds max length', () => {
      render(
        <SearchForm
          onResults={jest.fn()}
          numRecommendations={numRecommendations}
          maxTextLength={maxTextLength}
        />
      );

      fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'A'.repeat(maxTextLength + 1) } });
      expect(screen.getByText(new RegExp(maxTextLengthErrorMsg, 'i'))).toBeInTheDocument();
    });

    it('does not display an error when abstract length has max length', () => {
      render(
        <SearchForm
          onResults={jest.fn()}
          numRecommendations={numRecommendations}
          maxTextLength={maxTextLength}
        />
      );

      fireEvent.change(screen.getByLabelText(/Abstract/i), { target: { value: 'A'.repeat(maxTextLength) } });
      expect(screen.queryByText(new RegExp(maxTextLengthErrorMsg, 'i'))).not.toBeInTheDocument();
    });

    it('displays an error when abstract length exceeds max length', () => {
      render(
        <SearchForm
          onResults={jest.fn()}
          numRecommendations={numRecommendations}
          maxTextLength={maxTextLength}
        />
      );

      fireEvent.change(screen.getByLabelText(/Abstract/i), { target: { value: 'A'.repeat(maxTextLength + 1) } });
      expect(screen.getByText(new RegExp(maxTextLengthErrorMsg, 'i'))).toBeInTheDocument();
    });

    it('does not display an error when title and abstract length has max length', () => {
      render(
        <SearchForm
          onResults={jest.fn()}
          numRecommendations={numRecommendations}
          maxTextLength={maxTextLength}
        />
      );

      fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'A'.repeat(1) } });
      fireEvent.change(screen.getByLabelText(/Abstract/i), { target: { value: 'A'.repeat(maxTextLength - 1) } });
      expect(screen.queryByText(new RegExp(maxTextLengthErrorMsg, 'i'))).not.toBeInTheDocument();
    });

    it('displays an error when title and abstract length exceeds max length', () => {
      render(
        <SearchForm
          onResults={jest.fn()}
          numRecommendations={numRecommendations}
          maxTextLength={maxTextLength}
        />
      );

      fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'A'.repeat(1) } });
      fireEvent.change(screen.getByLabelText(/Abstract/i), { target: { value: 'A'.repeat(maxTextLength) } });
      expect(screen.getByText(new RegExp(maxTextLengthErrorMsg, 'i'))).toBeInTheDocument();
    });

    it('does not call fetchRecommendations when text exceeds max length on submit', () => {
      fetchRecommendations as jest.Mock;
      render(
        <SearchForm
          onResults={jest.fn()}
          numRecommendations={numRecommendations}
          maxTextLength={maxTextLength}
        />
      );

      fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'A'.repeat(maxTextLength + 1) } });
      fireEvent.click(screen.getByRole('button', { name: /Search/i }));
      expect(fetchRecommendations).not.toHaveBeenCalled();
    });
  });
  
  it('calls onResults when fetchRecommendations is called on valid input', async () => {
    const mockOnResults = jest.fn();
    const mockPapers = [{ title: 'Paper 1' }];

    (fetchRecommendations as jest.Mock).mockResolvedValue({ papers: mockPapers });
    render(<SearchForm onResults={mockOnResults} numRecommendations={numRecommendations} />);
    
    const title = 'Example title';
    const abstract = 'Example abstract';

    fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: title } });
    fireEvent.change(screen.getByLabelText(/Abstract/i), { target: { value: abstract } });
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    await waitFor(() => expect(fetchRecommendations).toHaveBeenCalledWith(title, abstract, numRecommendations));
    await waitFor(() => expect(mockOnResults).toHaveBeenCalledWith(mockPapers));
  });

  it('displays an error when fetchRecommendation fails', async () => {
    (fetchRecommendations as jest.Mock).mockRejectedValue(new Error('Network Error'));
    render(<SearchForm onResults={jest.fn()} numRecommendations={numRecommendations} />);

    fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'Example title' } });
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    expect(
      await screen.findByText(/Failed to fetch recommendations: Network Error/i)
    ).toBeInTheDocument();
  });

  it('displays a generic error when fetchRecommendations fails with a non-Error type', async () => {
    (fetchRecommendations as jest.Mock).mockRejectedValue('Unknown error');
    render(<SearchForm onResults={jest.fn()} numRecommendations={numRecommendations} />);

    fireEvent.change(screen.getByLabelText(/Title/i), { target: { value: 'Example title' } });
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    expect(await screen.findByText(/Failed to fetch recommendations/i)).toBeInTheDocument();
  });
});
