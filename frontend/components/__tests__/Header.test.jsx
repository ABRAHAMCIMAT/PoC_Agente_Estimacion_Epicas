import { render, screen } from '@testing-library/react';
import Header from '../Header';

describe('Header', () => {
  it('renderiza el título principal del sistema', () => {
    render(<Header />);

    expect(
      screen.getByText(/Sistema de Estimación de Épicas/i)
    ).toBeInTheDocument();
  });

  it('renderiza el subtítulo descriptivo', () => {
    render(<Header />);

    expect(
      screen.getByText(/puntos, duración, costo y esfuerzo/i)
    ).toBeInTheDocument();
  });
});
