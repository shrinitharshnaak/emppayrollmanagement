// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', validateForm);
    });

    // Date validation for leave request
    const startDate = document.getElementById('start_date');
    const endDate = document.getElementById('end_date');
    if (startDate && endDate) {
        endDate.addEventListener('change', () => {
            if (startDate.value > endDate.value) {
                alert('End date must be after start date');
                endDate.value = '';
            }
        });
    }

    // Payroll calculations
    const deductions = document.getElementById('deductions');
    const additions = document.getElementById('additions');
    if (deductions && additions) {
        [deductions, additions].forEach(input => {
            input.addEventListener('change', () => {
                if (input.value < 0) {
                    alert('Value cannot be negative');
                    input.value = 0;
                }
            });
        });
    }
});

function validateForm(e) {
    const requiredFields = e.target.querySelectorAll('[required]');
    let valid = true;
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            valid = false;
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }
    });
    if (!valid) {
        e.preventDefault();
        alert('Please fill all required fields');
    }
}