module fmesh

implicit none

integer, parameter:: dp=kind(0.d0)

contains

subroutine mesh_exp(r_min, r_max, a, N, mesh)
! Generates exponential mesh of N elements on [r_min, r_max]
! The meaning of the parameter "a" is the fraction of the largest/smallest
! elements in the mesh
real(dp), intent(in) :: r_min
real(dp), intent(in) :: r_max
real(dp), intent(in) :: a
integer, intent(in) :: N
real(dp), intent(out) :: mesh(N+1)

integer :: i
real(dp) :: alpha, beta
if (N > 1) then
    beta = log(a)/(N-1)
    alpha = (r_max - r_min) / (exp(N*beta) - 1)
    do i = 0, N
        mesh(i+1) = alpha * (exp(i*beta) - 1) + r_min
    enddo
else if (N == 1) then
    mesh(1) = r_min
    mesh(2) = r_max
else
    stop "mesh_log() requires N >= 1"
endif
end subroutine

subroutine mesh_hyp(r_min, r_max, a, N, mesh)
! Generates hyperbolic mesh of N elements on [r_min, r_max]
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
