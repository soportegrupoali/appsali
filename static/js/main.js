// JavaScript principal para SOTALI

document.addEventListener('DOMContentLoaded', function() {
    console.log('SOTALI - Sistema cargado correctamente');
    
    // Función para mostrar la fecha y hora actual
    function updateDateTime() {
        const now = new Date();
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        };
        
        const dateTimeString = now.toLocaleDateString('es-ES', options);
        
        // Actualizar elementos de fecha/hora
        const dateTimeElements = document.querySelectorAll('#currentDateTime, #currentDateTimeMobile');
        dateTimeElements.forEach(element => {
            if (element) {
                element.textContent = dateTimeString;
            }
        });
    }
    
    // Actualizar fecha y hora cada segundo
    updateDateTime();
    setInterval(updateDateTime, 1000);
    
    // Función para animar elementos al hacer scroll
    function animateOnScroll() {
        const elements = document.querySelectorAll('.card, .alert, .btn');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('fade-in-up');
            }
        });
    }
    
    // Ejecutar animación al hacer scroll
    window.addEventListener('scroll', animateOnScroll);
    
    // Función para validar formularios
    function validateForm(form) {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            }
        });
        
        return isValid;
    }
    
    // Aplicar validación a todos los formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(this)) {
                event.preventDefault();
                event.stopPropagation();
                
                // Scroll al primer campo inválido
                const firstInvalid = this.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
            }
        });
    });
    
    // Función para convertir RFC a mayúsculas
    const rfcInputs = document.querySelectorAll('input[name="rfc"]');
    rfcInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    });
    
    // Función para confirmar eliminaciones
    const deleteButtons = document.querySelectorAll('.btn-danger[type="submit"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('¿Está seguro que desea realizar esta acción? Esta operación no se puede deshacer.')) {
                event.preventDefault();
            }
        });
    });
    
    // Función para mostrar tooltips de Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Función para mostrar popovers de Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Función para cerrar alertas automáticamente
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
    
    // Función para mejorar la experiencia de búsqueda
    const searchInputs = document.querySelectorAll('input[name="search"]');
    searchInputs.forEach(input => {
        let searchTimeout;
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 2 || this.value.length === 0) {
                    this.closest('form').submit();
                }
            }, 500);
        });
    });
    
    // Función para mejorar la experiencia en dispositivos móviles
    function handleMobileMenu() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (navbarToggler && navbarCollapse) {
            // Cerrar menú al hacer clic en un enlace
            const navLinks = navbarCollapse.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (window.innerWidth < 992) {
                        navbarCollapse.classList.remove('show');
                    }
                });
            });
        }
    }
    
    handleMobileMenu();
    
    // Función para mejorar la accesibilidad
    function improveAccessibility() {
        // Agregar atributos ARIA a elementos dinámicos
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            if (!button.getAttribute('aria-label')) {
                const icon = button.querySelector('i');
                const text = button.textContent.trim();
                if (icon && text) {
                    button.setAttribute('aria-label', text);
                }
            }
        });
    }
    
    improveAccessibility();
    
    console.log('SOTALI - Funcionalidades JavaScript inicializadas');
});

// Función global para mostrar notificaciones
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Remover automáticamente después de 5 segundos
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Función global para confirmar acciones
function confirmAction(message = '¿Está seguro que desea realizar esta acción?') {
    return confirm(message);
}

// Función global para validar RFC
function validateRFC(rfc) {
    const rfcRegex = /^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$/;
    return rfcRegex.test(rfc);
}

// Función global para formatear RFC
function formatRFC(rfc) {
    return rfc.toUpperCase().replace(/[^A-Z0-9&Ñ]/g, '');
} 