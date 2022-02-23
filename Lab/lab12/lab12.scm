; macro 是先替换, 再 evaluate, 其中替换是把参数先 quote 了再扔进去, 不 evaluate
; quasiquote 就是 evaluate 逗号后面的整个表达式
(define-macro (def func args body)
  `(define ,(cons func args) ,body))

(define (map-stream f s)
  (if (null? s)
      nil
      (cons-stream (f (car s))
                   (map-stream f (cdr-stream s)))))

(define all-three-multiples
        (cons-stream 3
                     (map-stream (lambda (x) (+ x 3))
                                 all-three-multiples)))

(define (compose-all funcs)
  (if (null? funcs)
      (lambda (x) x)
      (lambda (x)
        ((compose-all (cdr funcs)) ((car funcs) x)))))

(define (partial-sums stream)
  (define (helper sum stream)
    (if (null? stream)
        nil
        (cons-stream (+ sum (car stream))
                     (helper (+ sum (car stream)) (cdr-stream stream)))))
  (helper 0 stream))
