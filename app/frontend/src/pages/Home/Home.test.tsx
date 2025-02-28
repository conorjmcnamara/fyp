import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Home from './Home';
import { PaperResponse } from '../../services/recommendationService';

jest.mock('../../components/Header/Header', () => () => <div>Header Mock</div>);
jest.mock(
  '../../components/SearchForm/SearchForm',
  () =>
    ({ onResults }: { onResults: (papers: PaperResponse[]) => void }) => (
      <div>
        <button
          onClick={() =>
            onResults([
              {
                id: '1',
                title: 'Paper 1',
                year: 2025,
                abstract: 'Abstract for paper 1',
                venue: 'Venue 1',
                authors: [{ first_name: 'John', last_name: 'Doe' }],
                recommendation_score: 95
              },
            ])
          }
        >
          Search
        </button>
      </div>
    )
);
jest.mock(
  '../../components/RecommendationResults/RecommendationResults',
  () =>
    ({ papers }: { papers: PaperResponse[] }) => (
      <div>
        {papers.map((paper) => (
          <div key={paper.id}>{paper.title}</div>
        ))}
      </div>
    )
);

describe('Home', () => {
  it('renders the Header and SearchForm components', () => {
    render(<Home />);

    expect(screen.getByText('Header Mock')).toBeInTheDocument();
    expect(screen.getByText('Search')).toBeInTheDocument();
  });

  it('renders RecommendationResults when papers are returned from SearchForm', async () => {
    render(<Home />);

    fireEvent.click(screen.getByText('Search'));

    await waitFor(() => expect(screen.getByText('Paper 1')).toBeInTheDocument());
  });

  it('does not render RecommendationResults when papers is empty', () => {
    render(<Home />);

    expect(screen.queryByText('Paper 1')).not.toBeInTheDocument();
  });
});

