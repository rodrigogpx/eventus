// Verifica se há uma preferência salva
const currentTheme = localStorage.getItem('theme');
if (currentTheme) {
    document.documentElement.setAttribute('data-theme', currentTheme);
}

// Função para alternar o tema
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Atualiza o ícone do botão
    const themeIcon = document.getElementById('theme-icon');
    themeIcon.className = newTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
}
