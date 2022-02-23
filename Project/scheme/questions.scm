(define (caar x) (car (car x)))

(define (cadr x) (car (cdr x)))

(define (cdar x) (cdr (car x)))

(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.
(define (cons-all first rests)
  (map (lambda (x) (append (list first) x)) rests))

(define (zip pairs)
  (list (map (lambda (x) (car x)) pairs)
        (map (lambda (x) (cadr x)) pairs)))

; ; Returns a list of two-element lists
(define (enumerate s)
  (define (enumerate-helper s i)
    (if (null? s)
        nil
        (cons (list i (car s))
              (enumerate-helper (cdr s) (+ i 1)))))
  (enumerate-helper s 0))

; ; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  (cond 
    ((null? denoms)
     nil)
    ((zero? total)
     (list nil))
    ((< total (car denoms))
     (list-change total (cdr denoms)))
    (else ; 这里就是看 denoms 的第一个要不要得起, 要不起就彻底扔掉, 否则还要保留
     (append (cons-all (car denoms)
                       (list-change (- total (car denoms)) denoms)) ; 注意这里还要保留完整的 denoms
             (list-change total (cdr denoms))))))

; ; Problem 18
; ; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))

(define define? (check-special 'define))

(define quoted? (check-special 'quote))

(define let? (check-special 'let))

; ; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond 
    ((atom? expr) ; 这个和下面的 quoted 是递归终点
     expr)
    ((quoted? expr) ; 因为这里只用转换表达式, 不用 evaluate, 所以 quoted 也返回自身
     ; 注意 quoted 不用递归转换, 否则就违背了 quoted 的本义
     expr)
    ((or (lambda? expr) (define? expr)) 
     ; 这里 form 和 params 都不用转换(有例子说 lambda parameters not affected), body 可能需要递归进行转换
     (let ((form (car expr))
           (params (cadr expr))
           (body (cddr expr)))
       (cons form (cons params (map let-to-lambda body)))))
    ((let? expr) ; form 换成 lambda, params 需要转换, body 递归转换, 之后还要调用这个 lambda
     ; 注意 zip 之前还要再递归转换, 因为参数里也可能有 let
     ; params 转换为 (car (zip(let-to-lambda values))), 调用时的参数为 (cadr (zip(let-to-lambda values)))
     (let ((values (cadr expr))
           (body (cddr expr)))
       (cons (cons 'lambda
             (cons (car (zip (let-to-lambda values)))
                             (map let-to-lambda body)))
                   (cadr (zip (let-to-lambda values))))))
    (else ; 函数体, 继续递归即可
     (map let-to-lambda expr))))
