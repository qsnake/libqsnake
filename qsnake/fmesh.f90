module fmesh

implicit none

integer, parameter:: dp=kind(0.d0)

contains

subroutine mesh_exp(r_min, r_max, a, N, mesh)
! Generates exponential mesh of N elements on [r_min, r_max]
!
! Input parameters:
!     r_min, r_max .... The domain [r_min, r_max], the mesh will contain both
!                       endpoints
!     a ............... The fraction of the rightmost vs. leftmost elements of
!                       the mesh (for a > 1 this means the "largest/smallest").
!                       The only requirement is a > 0. For a == 1 a uniform
!                       mesh will be returned.
!     N ............... The number of elements in the mesh
!
! Output parameters:
!     mesh(N+1) ....... The generated mesh
real(dp), intent(in) :: r_min
real(dp), intent(in) :: r_max
real(dp), intent(in) :: a
integer, intent(in) :: N
real(dp), intent(out) :: mesh(N+1)

integer :: i
real(dp) :: alpha, beta
if (a < 0) then
    stop "mesh_exp: a > 0 required"
else if (a == 1) then
    alpha = (r_max - r_min) / N
    do i = 1, N+1
        mesh(i) = alpha * (i-1.0_dp) + r_min
    enddo
else
    if (N > 1) then
        beta = log(a)/(N-1)
        alpha = (r_max - r_min) / (exp(beta*N) - 1)
        do i = 1, N+1
            mesh(i) = alpha * (exp(beta*(i-1)) - 1) + r_min
        enddo
    else if (N == 1) then
        mesh(1) = r_min
        mesh(2) = r_max
    else
        stop "mesh_exp: N >= 1 required"
    endif
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
