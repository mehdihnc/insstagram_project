function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

class PostInteractions {
    constructor() {
        this.setupLikeButtons();
        this.setupCommentForms();
    }

    setupLikeButtons() {
        document.querySelectorAll('.like-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleLike(button);
            });
        });
    }

    handleLike(button) {
        const postId = button.dataset.postId;
        const icon = button.querySelector('i');
        const likesCount = button.closest('.card-body').querySelector('.likes-count');
        
        fetch(`/interactions/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (data.is_liked) {
                    icon.classList.replace('far', 'fas');
                } else {
                    icon.classList.replace('fas', 'far');
                }
                likesCount.textContent = `${data.likes_count} j'aime${data.likes_count !== 1 ? 's' : ''}`;
            }
        })
        .catch(error => console.error('Erreur:', error));
    }

    setupCommentForms() {
        document.querySelectorAll('.comment-form').forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const postId = form.dataset.postId;
                const input = form.querySelector('input[name="content"]');
                if (input && input.value.trim()) {
                    this.handleComment(postId, input.value.trim(), form);
                }
            });
        });
    }

    async handleComment(postId, content, form) {
        try {
            const response = await fetch(`/interactions/comment/${postId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ content: content })
            });

            const data = await response.json();
            if (data.success) {
                let commentsSection = form.closest('.card-body').querySelector('.comments-section');
                if (!commentsSection) {
                    commentsSection = document.querySelector(`#comments-${postId}`);
                }
                
                if (commentsSection) {
                    const newComment = document.createElement('p');
                    newComment.className = 'mb-1';
                    newComment.innerHTML = `
                        <span class="fw-bold">${data.comment.username}</span>
                        ${data.comment.content}
                    `;
                    commentsSection.insertBefore(newComment, commentsSection.firstChild);
                }
                
                const input = form.querySelector('input[name="content"]');
                if (input) {
                    input.value = '';
                }
            }
        } catch (error) {
            console.error('Erreur lors de l\'ajout du commentaire:', error);
        }
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    new PostInteractions();
}); 