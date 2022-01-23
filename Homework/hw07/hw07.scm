(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
  (car (cddr s))
)


(define (sign num)
  (cond ((> num 0) 1)
    ((< num 0) -1)
    (else 0))
)


(define (square x) (* x x))

(define (pow x y)
  (if (= y 0)
    1
    (if (even? y)
      (square (pow x (/ y 2)))
      (* x (square (pow x (/ (- y 1) 2))))))
)


(define (unique s)
  (if (null? s)
    nil
    (cons (car s) (unique (filter
      (lambda (x) (if (eq? x (car s)) #f #t))  
      (cdr s))))
  )
)


(define (replicate x n)
  (define (helper s n)
    (if (= n 0)
      s
      (helper (cons x s) (- n 1))
    )
  )
  (helper nil n)
)


(define (accumulate combiner start n term)
  (if (= n 0)
    start
    (accumulate combiner (combiner start (term n)) (- n 1) term))
)


(define (accumulate-tail combiner start n term)
  (if (= n 0)
    start
    (accumulate combiner (combiner start (term n)) (- n 1) term))
)


(define-macro (list-of map-expr for var in lst if filter-expr)
  (list 'map (list 'lambda (list var) map-expr) (list 'filter (list 'lambda (list var) filter-expr) lst))
)

