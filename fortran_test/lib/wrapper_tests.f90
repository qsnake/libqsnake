subroutine args_subr1(a, b, c, d, o)
      integer(kind=1), intent(in) :: a
      integer(kind=2), intent(in) :: b
      integer(kind=4), intent(in) :: c
      integer(kind=8), intent(in) :: d
      integer(kind=8), intent(out) :: o

      o = a*1000 + b*100 + c*10 + d
end subroutine

function args_func1(a, b, c, d)
      integer(kind=8) :: args_func1
      integer(kind=1), intent(in) :: a
      integer(kind=2), intent(in) :: b
      integer(kind=4), intent(in) :: c
      integer(kind=8), intent(in) :: d

      args_func1 = a*1000 + b*100 + c*10 + d
end function

function int_arg(a, b, c)
    integer, intent(in) :: a
    integer, intent(in) :: b
    integer, intent(in) :: c

    integer tmp
    tmp = a
    tmp = c

    int_arg = b
end function

function single_arg(a, b, c)
      integer, parameter:: sp=kind(0.e0) ! single precision
      real(sp) :: single_arg
      real(sp), intent(in) :: a
      real(sp), intent(in) :: b
      real(sp), intent(in) :: c

      real(sp) tmp
      tmp = a
      tmp = c

      single_arg = b
end function

function double_arg(a, b, c)
      integer, parameter:: dp=kind(0.d0) ! double precision

      real(dp) :: double_arg
      real(dp), intent(in) :: a
      real(dp), intent(in) :: b
      real(dp), intent(in) :: c

      real(dp) tmp
      tmp = a
      tmp = c

      double_arg = b
end function

subroutine string_arg1(a)
      character(*) :: a
      character(len=32) :: sample_string = "This is a sample"//CHAR(0)

      a = sample_string
end subroutine

subroutine string_arg2(a, b, c)
      character(*) :: a
      character(*) :: b
      character(*) :: c

      character(len(a)) :: tmp

      tmp = a
      a = b
      b = c
      c = tmp
end subroutine

subroutine string_arg3(a, b, n1, c, n2)
      character(*) :: a
      character(*) :: b
      character(*) :: c
      integer :: n1
      integer :: n2

      character(len(a)) :: tmp

      tmp = a
      a = b
      b = c
      c = tmp

      n2 = n2 + n1
end subroutine

subroutine single_array1(a)
      integer, parameter:: sp=kind(0.e0) ! single precision

      ! expects assume size array of size 4:
      real(sp) :: a(*)

      a(1) = 1.1e0
      a(2) = 2.1e0
      a(3) = 3.1e0
      a(4) = 4.1e0
end subroutine

subroutine double_array1(a)
      integer, parameter:: dp=kind(0.d0) ! double precision

      ! expects assume size array of size 4:
      real(dp) :: a(*)

      a(1) = 1.1d0
      a(2) = 2.1d0
      a(3) = 3.1d0
      a(4) = 4.1d0
end subroutine

subroutine double_array2(a, n)
      integer, parameter:: dp=kind(0.d0) ! double precision

      ! expects assume size array of size 4:
      integer(kind=4), intent(in) :: n
      real(dp) :: a(n)

      integer i

      do i=1, n
          a(i) = i+0.1d0
      end do
end subroutine

subroutine int4_array1(a)
      ! expects assume size array of size 4:
      integer(kind=4) :: a(*)

      a(1) = 1
      a(2) = 2
      a(3) = 3
      a(4) = 4
end subroutine

subroutine int8_array1(a)
      ! expects assume size array of size 4:
      integer(kind=8) :: a(*)

      a(1) = 1
      a(2) = 2
      a(3) = 3
      a(4) = 4
end subroutine
