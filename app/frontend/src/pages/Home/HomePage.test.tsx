import React from 'react';
import { render, screen } from '@testing-library/react';
import HomePage from './HomePage';

describe('HomePage', () => {
  it('should render the Button component', () => {
    render(<HomePage />);

    expect(screen.getByRole('button', { name: /Get Message/i })).toBeInTheDocument();
  });
});
