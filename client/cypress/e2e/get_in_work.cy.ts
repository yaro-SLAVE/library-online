describe('Auth Flow', () => {
  beforeEach(() => {
    cy.visit('/profile')
  })

  it('should login with valid credentials', () => {
    cy.get('[data-cy="email"]').type('user@example.com')
    cy.get('[data-cy="password"]').type('password123')
    cy.get('[data-cy="submit"]').click()
    
    cy.url().should('include', '/dashboard')
    cy.get('[data-cy="welcome-message"]').should('contain', 'Welcome back')
  })

  it('should show error with invalid credentials', () => {
    cy.get('[data-cy="email"]').type('wrong@email.com')
    cy.get('[data-cy="password"]').type('wrongpass')
    cy.get('[data-cy="submit"]').click()
    
    cy.get('[data-cy="error-message"]').should('be.visible')
  })
})