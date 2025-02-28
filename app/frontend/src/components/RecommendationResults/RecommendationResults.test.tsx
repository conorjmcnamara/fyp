import { render, screen, fireEvent } from '@testing-library/react';
import RecommendationResults from './RecommendationResults';
import { PaperResponse } from '../../services/recommendationService';

const mockPapers: PaperResponse[] = [
  {
    id: '1',
    title: 'Paper 1',
    year: 2025,
    abstract: 'Abstract for paper 1',
    venue: 'Venue 1',
    authors: [{ first_name: 'John', last_name: 'Doe' }],
    recommendation_score: 95
  },
  {
    id: '2',
    title: 'Paper 2',
    year: 2025,
    abstract: 'Abstract for paper 2',
    venue: 'Venue 2',
    authors: [{ first_name: 'John', last_name: 'Doe' }],
    recommendation_score: 95
  }
]

describe('RecommendationResults', () => {
  it('renders only the specified number of papers per page', () => {
    render(<RecommendationResults papers={mockPapers} papersPerPage={1} />);

    expect(screen.getByText(/Paper 1/i)).toBeInTheDocument();
    expect(screen.queryByText(/Paper 2/i)).not.toBeInTheDocument();
  });

  it('paginates the next button correctly', () => {
    render(<RecommendationResults papers={mockPapers} papersPerPage={1} />);

    fireEvent.click(screen.getByRole('button', { name: /Next/i }));

    expect(screen.queryByText(/Paper 1/i)).not.toBeInTheDocument();
    expect(screen.getByText(/Paper 2/i)).toBeInTheDocument();

    expect(screen.getByRole('button', { name: /Next/i })).toBeDisabled();
  });

  it('paginates the prev button correctly', () => {
    render(<RecommendationResults papers={mockPapers} papersPerPage={1} />);

    expect(screen.getByRole('button', { name: /Prev/i })).toBeDisabled();

    fireEvent.click(screen.getByRole('button', { name: /Next/i }));
    fireEvent.click(screen.getByRole('button', { name: /Prev/i }));

    expect(screen.getByText(/Paper 1/i)).toBeInTheDocument();
    expect(screen.queryByText(/Paper 2/i)).not.toBeInTheDocument();
  });

  it('toggles abstract visibility', () => {
    render(<RecommendationResults papers={mockPapers} />);

    fireEvent.click(screen.getAllByText(/View Abstract/i)[0]);
    expect(screen.getByText(/Abstract for paper 1/i)).toBeInTheDocument();

    fireEvent.click(screen.getByText(/Hide Abstract/i));
    expect(screen.queryByText(/Abstract for paper 1/i)).not.toBeInTheDocument();
  });

  it('renders authors with commas except for the last author', () => {
    const paperWithAuthors = {
      ...mockPapers[0],
      authors: [
        { first_name: 'John', last_name: 'Doe' },
        { first_name: 'Jane', last_name: 'Smith' },
      ],
    };
    
    render(<RecommendationResults papers={[paperWithAuthors]} />);
    
    const johnDoe = screen.getByText(/John Doe/i);
    const janeSmith = screen.getByText(/Jane Smith/i);

    expect(johnDoe).toBeInTheDocument();
    expect(janeSmith).toBeInTheDocument();
    expect(johnDoe.textContent).toContain(','); 
    expect(janeSmith.textContent).not.toContain(',');
  });
});
