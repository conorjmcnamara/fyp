import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';
import { fetchMessage } from '../../services/messageService';

jest.mock('../../services/messageService');

describe('Button Component', () => {
  it('should render and fetch the message when clicked', async () => {
    (fetchMessage as jest.Mock).mockResolvedValue({ message: 'Hello'});
    render(<Button />);

    const button = screen.getByText(/Get Message/i);
    fireEvent.click(button);

    expect(screen.getByText(/Loading/i)).toBeInTheDocument();

    const message = await screen.findByText('Hello');
    expect(message).toBeInTheDocument();

    expect(screen.queryByText(/Loading/i)).not.toBeInTheDocument();
  });

  it('should show an error message if the API call fails', async() => {
    (fetchMessage as jest.Mock).mockRejectedValue(new Error('Failed to fetch message'));
    render(<Button />);

    const button = screen.getByText(/Get Message/i);
    fireEvent.click(button);

    const errorMessage = await screen.findByText(/Failed to fetch message/i);
    expect(errorMessage).toBeInTheDocument();

    expect(screen.queryByText(/Loading/i)).not.toBeInTheDocument();
  });
});
