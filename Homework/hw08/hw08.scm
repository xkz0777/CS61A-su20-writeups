(define (rle s)
    (define (helper times last s)
        (if (or (null? s) 
                (not (= (car s) last)))
            times
        (helper (+ times 1) last (cdr-stream s))))
    (define (remove s last)
        (if (null? s)
            nil
            (if (= last (car s))
                (remove (cdr-stream s) last)
                s)))
    (if (null? s)
        nil
        (cons-stream 
            (list (car s) (helper 0 (car s) s))
            (rle (remove s (car s))))))



(define (group-by-nondecreasing s)
    (define (helper s last)
        (if (or (null? s) (< (car s) last))
            nil
            (cons (car s) (helper (cdr-stream s) (car s)))))
    (define (remove s last)
        (if (or (null? s) (< (car s) last))
            s
            (remove (cdr-stream s) (car s))))
    (if (null? s)
        nil
        (cons-stream (helper s (car s)) (group-by-nondecreasing (remove s (car s))))))


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

