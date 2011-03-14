module fmesh

use iso_c_binding

implicit none

contains

subroutine c_mesh_log(r_min, r_max, a, N, mesh) bind(c)
real(c_double), intent(in) :: r_min
real(c_double), intent(in) :: r_max
real(c_double), intent(in) :: a
integer(c_int), intent(in) :: N
real(c_double), intent(out) :: mesh(N+1)
call mesh_log(r_min, r_max, a, N, mesh)
end subroutine

subroutine c_mesh_exp(r_min, r_max, a, N, mesh) bind(c)
real(c_double), intent(in) :: r_min
real(c_double), intent(in) :: r_max
real(c_double), intent(in) :: a
integer(c_int), intent(in) :: N
real(c_double), intent(out) :: mesh(N+1)
call mesh_exp(r_min, r_max, a, N, mesh)
end subroutine

end module
