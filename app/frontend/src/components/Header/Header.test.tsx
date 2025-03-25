import { render, screen } from '@testing-library/react';
import Header from './Header';

describe('Header component', () => {
  it('renders the header with a title and description', () => {
    render(<Header />);

    expect(screen.getByText(/Citation Recommender/i)).toBeInTheDocument();
    expect(screen.getByText(/Find relevant citations for your research/i)).toBeInTheDocument();
  });
});
