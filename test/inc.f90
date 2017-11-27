 ! test
        program main
            include "./inc1.inc"
            do a = 1, &
            &3
                do b = 1, 3
                    c = myadd(a, b)
                    print *, a, "abc""de&
                    &f""ghi", c
                end do
            end do
        contains
            function &
            &myadd(d, e) &
            &result(f)
                implicit none
                integer, intent(in) :: d, e
                integer :: f
                f = &
                &d + e; f & !test
!test
                &= "e& !test
                &" + d !test
            end function
        end program
