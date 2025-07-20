// Enhanced JavaScript for CardioPredict AI

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupFormValidation();
    setupProgressTracking();
    setupScrollAnimations();
    setupSmoothScrolling();
    setupFormSubmission();
    setupTooltips();
    setupAccessibility();
}

// Form validation and enhancement
function setupFormValidation() {
    const form = document.getElementById('predictionForm');
    const inputs = form.querySelectorAll('input, select');

    inputs.forEach(input => {
        // Real-time validation
        input.addEventListener('input', function() {
            validateField(this);
            updateProgress();
        });

        input.addEventListener('change', function() {
            validateField(this);
            updateProgress();
        });

        // Enhanced focus effects
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const min = parseFloat(field.min);
    const max = parseFloat(field.max);
    const numValue = parseFloat(value);

    // Remove previous validation classes
    field.classList.remove('border-red-500', 'border-green-500');

    if (!value) {
        field.classList.add('border-gray-200');
        return false;
    }

    // Validate numeric ranges
    if (field.type === 'number' && (numValue < min || numValue > max)) {
        field.classList.add('border-red-500');
        showFieldError(field, `Value must be between ${min} and ${max}`);
        return false;
    }

    field.classList.add('border-green-500');
    hideFieldError(field);
    return true;
}

function showFieldError(field, message) {
    const errorId = field.id + '_error';
    let errorElement = document.getElementById(errorId);
    
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.id = errorId;
        errorElement.className = 'text-red-500 text-sm mt-1';
        field.parentElement.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
}

function hideFieldError(field) {
    const errorId = field.id + '_error';
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.remove();
    }
}

// Progress tracking
function setupProgressTracking() {
    updateProgress();
}

function updateProgress() {
    const form = document.getElementById('predictionForm');
    const inputs = form.querySelectorAll('input[required], select[required]');
    const filled = Array.from(inputs).filter(input => input.value.trim() !== '').length;
    const progress = (filled / inputs.length) * 100;
    
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        progressBar.style.width = progress + '%';
        
        // Change color based on progress
        if (progress < 33) {
            progressBar.className = 'h-full transition-all duration-500 bg-gradient-to-r from-red-400 to-orange-400';
        } else if (progress < 66) {
            progressBar.className = 'h-full transition-all duration-500 bg-gradient-to-r from-yellow-400 to-orange-400';
        } else {
            progressBar.className = 'h-full transition-all duration-500 bg-gradient-to-r from-green-400 to-blue-500';
        }
    }
}

// Scroll animations
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe animated elements
    const animatedElements = document.querySelectorAll('.animate-slide-up, .form-group, .scroll-animate');
    animatedElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = `all 0.6s ease ${index * 0.1}s`;
        observer.observe(element);
    });
}

// Smooth scrolling
function setupSmoothScrolling() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form submission
function setupFormSubmission() {
    const form = document.getElementById('predictionForm');
    form.addEventListener('submit', handleFormSubmission);
}

async function handleFormSubmission(e) {
    e.preventDefault();
    
    if (!validateAllFields()) {
        showNotification('Please fill in all required fields correctly.', 'error');
        return;
    }

    const formData = collectFormData();
    await submitPrediction(formData);
}

function validateAllFields() {
    const form = document.getElementById('predictionForm');
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });

    return isValid;
}

function collectFormData() {
    const formData = new FormData(document.getElementById('predictionForm'));
    const data = {};

    for (let [key, value] of formData.entries()) {
        if (['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
             'thalach', 'exang', 'slope', 'ca', 'thal'].includes(key)) {
            data[key] = key === 'oldpeak' ? parseFloat(value) : parseInt(value);
        } else if (key === 'oldpeak') {
            data[key] = parseFloat(value);
        } else {
            data[key] = value;
        }
    }

    return data;
}

async function submitPrediction(data) {
    const submitBtn = document.getElementById('submitBtn');
    const loader = submitBtn.querySelector('.loader');
    const btnText = submitBtn.querySelector('.btn-text');
    
    try {
        setLoadingState(true);
        
        // Add loading animation
        submitBtn.disabled = true;
        btnText.style.opacity = '0';
        loader.classList.remove('hidden');

        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        displayResult(result);
        
        // Track analytics (if needed)
        trackPrediction(result);

    } catch (error) {
        console.error('Prediction error:', error);
        showError('Unable to connect to the prediction server. Please check your connection and try again.');
    } finally {
        setLoadingState(false);
        submitBtn.disabled = false;
        btnText.style.opacity = '1';
        loader.classList.add('hidden');
    }
}

function setLoadingState(isLoading) {
    const submitBtn = document.getElementById('submitBtn');
    if (isLoading) {
        submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
        submitBtn.innerHTML = `
            <div class="flex items-center justify-center">
                <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-2"></div>
                <span>Analyzing...</span>
            </div>
        `;
    } else {
        submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
        submitBtn.innerHTML = `
            <span class="btn-text relative z-10">
                <i class="fas fa-brain mr-3"></i>
                Analyze with AI
            </span>
        `;
    }
}

function displayResult(data) {
    const result = document.getElementById('result');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    
    const isRisk = data.prediction === 'Risk' || data.prediction === 1;
    
    // Add entrance animation
    result.classList.remove('hidden');
    result.classList.add('result-enter');
    
    if (isRisk) {
        resultIcon.innerHTML = '⚠️';
        resultTitle.textContent = 'Risk Detected';
        resultTitle.className = 'text-3xl font-bold mb-4 text-red-600';
        resultMessage.innerHTML = `
            <div class="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fas fa-exclamation-triangle text-red-400"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-red-800 font-semibold">Increased Risk Detected</p>
                        <p class="text-red-700 mt-1">Our AI analysis indicates an elevated risk of heart disease based on your medical profile.</p>
                    </div>
                </div>
            </div>
            <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fas fa-user-md text-blue-400"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-blue-800 font-semibold">Recommended Actions:</p>
                        <ul class="text-blue-700 mt-2 space-y-1">
                            <li>• Schedule an appointment with a cardiologist immediately</li>
                            <li>• Discuss comprehensive cardiac screening</li>
                            <li>• Review and modify lifestyle factors</li>
                            <li>• Monitor blood pressure and cholesterol regularly</li>
                            <li>• Consider stress management techniques</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    } else {
        resultIcon.innerHTML = '✅';
        resultTitle.textContent = 'Low Risk Assessment';
        resultTitle.className = 'text-3xl font-bold mb-4 text-green-600';
        resultMessage.innerHTML = `
            <div class="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fas fa-check-circle text-green-400"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-green-800 font-semibold">Low Risk Detected</p>
                        <p class="text-green-700 mt-1">Excellent! Your current medical profile suggests a lower risk of heart disease.</p>
                    </div>
                </div>
            </div>
            <div class="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <i class="fas fa-heart text-blue-400"></i>
                    </div>
                    <div class="ml-3">
                        <p class="text-blue-800 font-semibold">Maintain Heart Health:</p>
                        <ul class="text-blue-700 mt-2 space-y-1">
                            <li>• Continue regular physical activity</li>
                            <li>• Maintain a balanced, heart-healthy diet</li>
                            <li>• Keep up with routine medical check-ups</li>
                            <li>• Monitor key health metrics annually</li>
                            <li>• Manage stress levels effectively</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }

    // Add confidence score if available
    if (data.confidence) {
        const confidenceDiv = document.createElement('div');
        confidenceDiv.className = 'mt-4 p-4 bg-purple-50 border border-purple-200 rounded-lg';
        confidenceDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-brain text-purple-500 mr-3"></i>
                <div>
                    <p class="text-purple-800 font-semibold">AI Confidence Level</p>
                    <div class="mt-2">
                        <div class="bg-purple-200 rounded-full h-2">
                            <div class="bg-purple-500 h-2 rounded-full transition-all duration-1000" style="width: ${(data.confidence * 100).toFixed(1)}%"></div>
                        </div>
                        <p class="text-purple-700 text-sm mt-1">${(data.confidence * 100).toFixed(1)}% confidence in this assessment</p>
                    </div>
                </div>
            </div>
        `;
        resultMessage.appendChild(confidenceDiv);
    }

    // Scroll to result
    setTimeout(() => {
        result.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

function showError(message) {
    const result = document.getElementById('result');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    
    result.classList.remove('hidden');
    result.classList.add('result-enter');
    
    resultIcon.innerHTML = '❌';
    resultTitle.textContent = 'Analysis Error';
    resultTitle.className = 'text-3xl font-bold mb-4 text-red-600';
    resultMessage.innerHTML = `
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-800 font-semibold mb-2">⚠️ Unable to Complete Analysis</p>
            <p class="text-red-700">${message}</p>
            <div class="mt-4 p-3 bg-gray-50 rounded border-l-4 border-gray-400">
                <p class="text-gray-700 text-sm">
                    <strong>Troubleshooting:</strong><br>
                    • Check your internet connection<br>
                    • Refresh the page and try again<br>
                    • Contact support if the issue persists
                </p>
            </div>
        </div>
    `;
    
    setTimeout(() => {
        result.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full ${
        type === 'error' ? 'bg-red-500 text-white' : 
        type === 'success' ? 'bg-green-500 text-white' : 
        'bg-blue-500 text-white'
    }`;
    
    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas ${type === 'error' ? 'fa-exclamation-circle' : type === 'success' ? 'fa-check-circle' : 'fa-info-circle'} mr-2"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Tooltips
function setupTooltips() {
    const tooltips = {
        'cp': 'Different types of chest pain can indicate various cardiac conditions',
        'trestbps': 'Normal range is typically 90-140 mmHg',
        'chol': 'Total cholesterol levels - optimal is less than 200 mg/dL',
        'fbs': 'Fasting blood sugar above 120 mg/dL may indicate diabetes',
        'restecg': 'Electrocardiogram results showing heart rhythm patterns',
        'thalach': 'Maximum heart rate achieved during exercise stress test',
        'exang': 'Chest pain triggered by physical exertion',
        'oldpeak': 'ST segment depression on ECG during exercise',
        'slope': 'Shape of the ST segment on exercise ECG',
        'ca': 'Number of coronary arteries with significant blockage',
        'thal': 'Inherited blood disorder affecting oxygen transport'
    };

    Object.keys(tooltips).forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.title = tooltips[id];
            
            // Enhanced tooltip on hover
            element.addEventListener('mouseenter', function(e) {
                showTooltip(e, tooltips[id]);
            });
            
            element.addEventListener('mouseleave', hideTooltip);
        }
    });
}

function showTooltip(event, text) {
    const tooltip = document.createElement('div');
    tooltip.id = 'custom-tooltip';
    tooltip.className = 'fixed z-50 px-3 py-2 text-sm bg-gray-800 text-white rounded shadow-lg pointer-events-none';
    tooltip.textContent = text;
    tooltip.style.left = event.pageX + 10 + 'px';
    tooltip.style.top = event.pageY - 30 + 'px';
    
    document.body.appendChild(tooltip);
}

function hideTooltip() {
    const tooltip = document.getElementById('custom-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Accessibility improvements
function setupAccessibility() {
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const result = document.getElementById('result');
            if (!result.classList.contains('hidden')) {
                resetForm();
            }
        }
    });

    // Focus management
    const form = document.getElementById('predictionForm');
    const inputs = form.querySelectorAll('input, select');
    
    inputs.forEach((input, index) => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && index < inputs.length - 1) {
                e.preventDefault();
                inputs[index + 1].focus();
            }
        });
    });
}

// Utility functions
function resetForm() {
    const form = document.getElementById('predictionForm');
    const result = document.getElementById('result');
    
    form.reset();
    result.classList.add('hidden');
    result.classList.remove('result-enter');
    
    // Clear all error states
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.classList.remove('border-red-500', 'border-green-500');
        input.classList.add('border-gray-200');
        hideFieldError(input);
    });
    
    updateProgress();
    
    // Smooth scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    showNotification('Form reset successfully', 'success');
}

function trackPrediction(result) {
    // Analytics tracking (implement as needed)
    console.log('Prediction completed:', {
        timestamp: new Date().toISOString(),
        prediction: result.prediction,
        confidence: result.confidence
    });
}

// Global functions for inline event handlers
window.scrollToAssessment = function() {
    document.getElementById('assessment').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
};

window.findDoctors = function() {
    const result = document.getElementById('result');
    result.classList.add('hidden');
    document.getElementById('doctors').scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
    });
};

window.resetForm = resetForm;

// Performance optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Debounced progress update
window.updateProgress = debounce(updateProgress, 100);