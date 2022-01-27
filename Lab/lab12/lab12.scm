
(define-macro (def func args body)
    `(define ,func (lambda ,args ,body)))


(define (map-stream f s)
    (if (null? s)
    	nil
    	(cons-stream (f (car s)) (map-stream f (cdr-stream s)))))

(define ones (cons-stream 1 ones))

(def add-stream(x y) 
  (cons-stream (+ (car x) (car y))
    (add-stream (cdr-stream x) (cdr-stream y))))

(define int (cons-stream 1 (add-stream ones int)))

; 本版本不重复造轮子
(define all-three-multiples
  (map-stream (lambda (x) (* x 3)) int)
)

; 本版本比较正经(指题目要求 Do not define any other helper functions.)
(define all-three-multiples
  (cons-stream 3 
    (map-stream (lambda (x) (+ x 3)) all-three-multiples))
)

(define (compose-all funcs)
  (if (null? funcs)
    (lambda (x) x)
    (lambda (x) ((compose-all (cdr funcs)) ((car funcs) x))))
)


(define (partial-sums stream)
  (def helper(sum-now s)
    (if (null? s) nil ; if is finite
      (cons-stream (+ sum-now (car s))
        (helper (+ sum-now (car s)) (cdr-stream s))))
  )
  (helper 0 stream)
)

