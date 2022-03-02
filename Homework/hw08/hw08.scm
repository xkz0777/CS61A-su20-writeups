(define (rle s)
    (define (helper last times s)
        (if (null? s)
            (cons-stream (list last times) nil)
            (if (= last (car s))
                (helper last (+ times 1) (cdr-stream s))
                (cons-stream 
                    (list last times) (rle s)))))
       
    (if (null? s)
        nil
        (helper (car s) 1 (cdr-stream s))))



(define (group-by-nondecreasing s)
    (define (helper s last group)
        (if (null? s)
            (cons-stream group nil)
            (if (>= (car s) last)
                (helper (cdr-stream s) (car s) (append group (list (car s))))
                (cons-stream group (group-by-nondecreasing s)))))
    (if (null? s)
        nil
        (helper (cdr-stream s) (car s) (list(car s)))))


(define finite-test-stream
    (cons-stream 1
        (cons-stream 2
            (cons-stream 3
                (cons-stream 1
                    (cons-stream 2
                        (cons-stream 2
                            (cons-stream 1 nil))))))))

(define infinite-test-stream
    (cons-stream 1
        (cons-stream 2
            (cons-stream 2
                infinite-test-stream))))

