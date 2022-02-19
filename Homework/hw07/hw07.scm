(define (cddr s) (cdr (cdr s)))

(define (cadr s) (car (cdr s)))

(define (caddr s) (car (cdr (cdr s))))

(define (sign num)
  (cond 
    ((> num 0)   1)
    ((zero? num) 0)
    (else        -1)))

(define (square x) (* x x))

(define (pow x y)
  (cond 
    ((zero? y) 1)
    ((odd? y)  (* x (pow x (- y 1))))
    (else      (square (pow x (/ y 2))))))

(define (unique s)
  (if (null? s)
      nil
      (cons (car s)
            (unique (filter
                     (lambda (element) (not (eq? (car s) element)))
                     (cdr s))))))

(define (replicate x n)
  (define (helper lst n)
    (if (zero? n)
        lst
        (helper (append (cons x nil) lst) (- n 1))))
  (helper nil n))

(define (accumulate combiner start n term)
  (if (zero? n)
      start
      (accumulate combiner
                  (combiner start (term n))
                  (- n 1)
                  term)))

(define (accumulate-tail combiner start n term)
  (if (zero? n)
      start
      (accumulate combiner
                  (combiner start (term n))
                  (- n 1)
                  term)))

(define-macro
 (list-of map-expr for var in lst if filter-expr)
 `(map (lambda (,var) ,map-expr)
       (filter (lambda (,var) ,filter-expr) ,lst)))
