(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))



;; Problem 17
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 17
  (define (helper s n)
    (if (null? s)
      s
      (cons (list n (car s)) (helper (cdr s) (+ n 1))))
  )
  (helper s 0)
)
; END PROBLEM 17

;; Problem 18

(define (zip pairs)
  ; BEGIN PROBLEM 18
  (list (map car pairs) (map cadr pairs))
)
; END PROBLEM 18


;; Problem 19
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let? (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
          ; BEGIN PROBLEM 19
          expr
          ; END PROBLEM 19
        )
    ((quoted? expr)
      ; BEGIN PROBLEM 19

      expr
      ; END PROBLEM 19
    )
    ((or (lambda? expr)
       (define? expr))
      (let ((form (car expr))
             (params (cadr expr))
             (body (cddr expr)))
        ; BEGIN PROBLEM 19
        (cons form (cons params (map let-to-lambda body)))
        ; recursive call
        ; END PROBLEM 19
      ))
    ((let? expr)
      (let ((values (cadr expr))
             (body (cddr expr)))
        ; BEGIN PROBLEM 19
        (define zip_values (zip values))
        (cons (cons
                  'lambda (cons (car (zip values))
                            (map let-to-lambda body)))
          (map let-to-lambda (cadr zip_values)))
        ; END PROBLEM 19
      ))
    (else
      ; BEGIN PROBLEM 19
      (map let-to-lambda expr)
      ; END PROBLEM 19
    )))
