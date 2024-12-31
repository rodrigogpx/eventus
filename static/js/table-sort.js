// Funcionalidade de ordenação da tabela
function initTableSort() {
    const getCellValue = (tr, idx) => {
        const cell = tr.children[idx];
        // Remover badges e outros elementos HTML para ordenação
        return cell.innerText || cell.textContent;
    };
    
    const comparer = (idx, asc) => (a, b) => ((v1, v2) => {
        // Remover espaços em branco e caracteres especiais
        v1 = v1.trim();
        v2 = v2.trim();
        
        // Tentar converter para data no formato dd/mm/yyyy
        const date1 = v1.match(/^\d{2}\/\d{2}\/\d{4}$/);
        const date2 = v2.match(/^\d{2}\/\d{2}\/\d{4}$/);
        
        if (date1 && date2) {
            const [d1, m1, y1] = v1.split('/');
            const [d2, m2, y2] = v2.split('/');
            const dateObj1 = new Date(y1, m1 - 1, d1);
            const dateObj2 = new Date(y2, m2 - 1, d2);
            return dateObj1 - dateObj2;
        }
        
        // Tentar converter para número se ambos os valores forem numéricos
        if (v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2)) {
            return parseFloat(v1) - parseFloat(v2);
        }
        
        // Caso contrário, usar comparação de string
        return v1.toString().localeCompare(v2);
    })(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));
    
    document.querySelectorAll('th.sortable').forEach(th => {
        th.addEventListener('click', function() {
            const table = th.closest('table');
            const tbody = table.querySelector('tbody');
            const currentIdx = Array.from(th.parentNode.children).indexOf(th);
            
            // Toggle sort direction
            this.asc = !this.asc;
            
            // Sort the rows
            Array.from(tbody.querySelectorAll('tr'))
                .sort(comparer(currentIdx, this.asc))
                .forEach(tr => tbody.appendChild(tr));
            
            // Update sort indicators
            table.querySelectorAll('th.sortable').forEach(header => {
                header.classList.remove('asc', 'desc');
            });
            th.classList.toggle('asc', this.asc);
            th.classList.toggle('desc', !this.asc);
        });
    });
}

// Inicializar ordenação quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', initTableSort);
