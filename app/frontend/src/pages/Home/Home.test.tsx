import { render, screen, fireEvent } from '@testing-library/react';
import Home from './Home';
import { PaperResponse } from '../../services/recommendationService';

jest.mock('../../components/Header/Header', () => () => <div>Header component</div>);

jest.mock(
  '../../components/TabToggle/TabToggle',
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
              }
            ])
          }
        >
          TabToggle component
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
  it('renders the Header and TabToggle components', () => {
    render(<Home />);

    expect(screen.getByText(/Header component/i)).toBeInTheDocument();
    expect(screen.getByText(/TabToggle component/i)).toBeInTheDocument();
  });

  it('renders RecommendationResults when papers are returned from TabToggle', async () => {
    render(<Home />);

    fireEvent.click(screen.getByText(/TabToggle component/i));
    expect(await screen.findByText(/Paper 1/i)).toBeInTheDocument();
  });

  it('does not render RecommendationResults when papers is empty', () => {
    render(<Home />);

    expect(screen.queryByText(/Paper 1/i)).not.toBeInTheDocument();
  });
});

