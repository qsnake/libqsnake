module fmesh

use iso_c_binding

implicit none

integer, parameter:: dp=kind(0.d0)

contains

subroutine c_mesh_log(r_min, r_max, a, N, mesh) bind(c)
real(c_double), intent(in) :: r_min
real(c_double), intent(in) :: r_max
real(c_double), intent(in) :: a
integer(c_int), intent(in) :: N
real(c_double), intent(out) :: mesh(N+1)
call mesh_log(r_min, r_max, a, N, mesh)
end subroutine

subroutine mesh_log(r_min, r_max, a, N, mesh)
real(dp), intent(in) :: r_min
real(dp), intent(in) :: r_max
real(dp), intent(in) :: a
integer, intent(in) :: N
real(dp), intent(out) :: mesh(N+1)

real(dp) :: a_new
if (N > 1) then
    a_new = a**(N/(N-1.0_dp))
else if (N == 1) then
    a_new = a
else
    stop "mesh_log() requires N >= 1"
endif
call mesh_exp(r_min, r_max, a, N, mesh)
end subroutine

subroutine mesh_exp(r_min, r_max, a, N, mesh)
real(dp), intent(in) :: r_min
real(dp), intent(in) :: r_max
real(dp), intent(in) :: a
integer, intent(in) :: N
real(dp), intent(out) :: mesh(N+1)

integer :: i
if (N < 1) stop "mesh_exp() requires N >= 1"
do i = 0, N
    mesh(i+1) = i * (a - 1) / (a*N - i)  * (r_max - r_min) + r_min
enddo
end subroutine

end module
