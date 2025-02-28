import { render, screen } from '@testing-library/react';
import Header from './Header';

describe('Header component', () => {
  it('renders the header with a title and description', () => {
    render(<Header />);

    const titleElement = screen.getByText(/Citation Recommender/i);
    expect(titleElement).toBeInTheDocument();

    const descriptionElement = screen.getByText(/Find relevant citations for your research/i);
    expect(descriptionElement).toBeInTheDocument();
  });
});
