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

integer :: i
do i = 1, N+1
    mesh(i) = i
enddo
end subroutine

end module
